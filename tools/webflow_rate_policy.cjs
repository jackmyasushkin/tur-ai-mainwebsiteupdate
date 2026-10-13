class WebflowRatePolicy {
  static responseInfo(response) {
    // MCP can return an HTTP failure inside a text block without isError.
    const raw = JSON.stringify(response);
    const is429 = /Too Many Requests|too_many_requests|RATE_LIMITED|returned\s*429|status.{0,12}429|rate.limit.exceeded/i.test(raw);
    const headers = {};
    const visit = value => {
      if (!value || typeof value !== 'object') return;
      for (const [key, child] of Object.entries(value)) {
        const name = key.toLowerCase();
        if (['retry-after', 'x-ratelimit-limit', 'x-ratelimit-remaining'].includes(name)) headers[name] = child;
        if (key === 'text' && typeof child === 'string') {
          try { visit(JSON.parse(child)); } catch { /* Plain diagnostic text. */ }
        } else visit(child);
      }
    };
    visit(response);
    return {is429, retryAfter:headers['retry-after'], limit:Number(headers['x-ratelimit-limit']) || null, remaining:headers['x-ratelimit-remaining'] ?? null};
  }
  static waitMs(s, weight, now) {
    if (!Number.isInteger(weight) || weight < 1 || weight > 10) throw new Error('Batch must have 1..10 operations');
    s.events = s.events.filter(e => now - e.at < 60000);
    let wait = Math.max(0, s.lastEnd + 2000 - now, s.cooldownUntil - now);
    let used = s.events.reduce((n,e) => n + e.weight, 0);
    if (used + weight > s.budget) {
      for (const e of [...s.events].sort((a,b)=>a.at-b.at)) {
        used -= e.weight;
        wait = Math.max(wait, e.at + 60000 - now);
        if (used + weight <= s.budget) break;
      }
    }
    return wait;
  }
  static finish(s, weight, now) { s.events.push({at:now,weight}); s.lastEnd=now; }
  static rateLimited(s, retryAfter, now) {
    s.rateErrors += 1; s.budget = Math.min(s.budget,15);
    let ms = Number(retryAfter) * 1000;
    if (!Number.isFinite(ms) || ms <= 0) ms = Date.parse(retryAfter) - now;
    if (!Number.isFinite(ms) || ms <= 0) ms = 60000 * 2 ** Math.min(s.rateErrors-1,2);
    s.cooldownUntil = now + ms + 2000;
    return {waitMs:ms+2000,stop:s.rateErrors>=4};
  }
  static reconcile(expected, actual) {
    return expected.map(e=>({id:e.id,status:actual[e.id]===e.after?'applied':actual[e.id]===e.before?'retry':'conflict'}));
  }
}
module.exports = WebflowRatePolicy;
