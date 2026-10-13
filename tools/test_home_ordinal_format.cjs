const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const source = fs.readFileSync(path.join(__dirname, '../webflow/home-ordinal-format.js'), 'utf8');

function fixture(readyState = 'complete') {
  const jobs = [], observers = [], listeners = [];
  let writes = 0;
  class TextElement {
    constructor(text, marked = true, count = true) { this.text = text; this.marked = marked; this.count = count; this.listeners = []; }
    get textContent() { return this.text; }
    set textContent(value) { this.text = String(value); writes++; this.listeners.forEach(callback => jobs.push(callback)); }
  }
  const ordinals = ['01','02','03','04'].map(text => new TextElement(text));
  const metrics = ['62','82','83','3'].map(text => new TextElement(text, false));
  const excluded = new TextElement('3', true, false);
  const nodes = [...ordinals, ...metrics, excluded];
  class MutationObserver {
    constructor(callback) { this.callback = callback; observers.push(this); }
    observe(element, options) { this.element = element; this.options = options; element.listeners.push(this.callback); }
  }
  const document = {
    readyState,
    querySelectorAll(selector) {
      assert.equal(selector, '[data-tur-number-format="ordinal-2"][fs-numbercount-element="number"]');
      return nodes.filter(node => node.marked && node.count);
    },
    addEventListener(event, callback, options) { assert.equal(event, 'DOMContentLoaded'); assert.equal(options.once, true); listeners.push(callback); }
  };
  const context = vm.createContext({document, MutationObserver});
  const run = () => vm.runInContext(source, context);
  const flush = () => {
    let deliveries = 0;
    while (jobs.length) { if (++deliveries > 20) throw Error('Observer failed to settle'); jobs.shift()(); }
    return deliveries;
  };
  return {nodes,ordinals,metrics,excluded,observers,listeners,context,document,run,flush,writes:()=>writes};
}

const f = fixture('loading');
f.run();
assert.equal(f.observers.length, 4);
assert.equal(f.writes(), 0, 'correct source remains untouched without Finsweet');
for (const observer of f.observers) assert.deepEqual({...observer.options}, {childList:true,characterData:true,subtree:true});
f.listeners.forEach(callback => callback());
f.run();
assert.equal(f.observers.length, 4, 'DOMContentLoaded and duplicate execution do not double observers');

for (const frame of [0,1,2,3,4,9,10,99]) {
  f.ordinals.forEach(node => {node.textContent = String(frame);});
  assert.equal(f.flush(), frame < 10 ? 8 : 4, 'one bounded formatting write per changed node');
  assert.deepEqual(f.ordinals.map(node=>node.textContent), Array(4).fill(String(frame).padStart(2,'0')));
}
for (const text of ['100','-1','3.0','', ' 3', 'abc','01.']) {
  f.ordinals[0].textContent = text; f.flush();
  assert.equal(f.ordinals[0].textContent, text, 'non-ordinal text is not silently rewritten');
}
f.metrics[3].textContent = '0'; f.flush();
assert.equal(f.metrics[3].textContent, '0', 'metric intermediate values remain single digit');
assert.equal(f.excluded.textContent, '3', 'marker alone does not capture a different element');
f.ordinals.forEach((node,i)=>{node.textContent=String(i+1);}); f.flush();
assert.deepEqual(f.ordinals.map(node=>node.textContent), ['01','02','03','04']);

// Optional integration check executes the actual downloaded, unchanged v1 library.
const libraryIndex = process.argv.indexOf('--library');
if (libraryIndex !== -1) {
  const g = fixture();
  const raf = [], intersections = [];
  g.nodes = g.nodes.slice(0,8);
  const url = 'https://cdn.jsdelivr.net/npm/@finsweet/attributes-numbercount@1/numbercount.js';
  const script = {src:url,getAttribute(){return null;}};
  g.document.currentScript = script;
  const select = g.document.querySelectorAll;
  g.document.querySelectorAll = selector => selector.startsWith('script') ? [script] : selector.includes('data-tur-number-format') ? select(selector) : g.nodes;
  for (const node of g.nodes) {
    node.attrs = {};
    node.getAttribute = key => key === 'fs-numbercount-element' ? 'number' : null;
    node.setAttribute = (key,value) => {node.attrs[key]=value;};
    node.hasAttribute = key => key in node.attrs;
    node.getBoundingClientRect = () => ({top:0});
  }
  Object.assign(g.context, {
    URL, setTimeout, clearTimeout,
    window:{location:{href:'https://example.webflow.io/'},innerHeight:900,Webflow:[],addEventListener(){},removeEventListener(){}},
    requestAnimationFrame(callback){raf.push(callback);},
    IntersectionObserver:class {
      constructor(callback){this.callback=callback;intersections.push(this);}
      observe(node){this.node=node;} disconnect(){}
    }
  });
  (async()=>{
    g.run();
    vm.runInContext(fs.readFileSync(process.argv[libraryIndex+1], 'utf8'),g.context);
    for(const init of g.context.window.Webflow)await init();
    intersections.forEach(observer=>observer.callback([{isIntersecting:true,intersectionRect:{top:0}}]));
    const timeline=[];
    for(const milliseconds of [0,250,500,750,1000]) {
      for(const frame of raf.splice(0))frame(milliseconds);
      g.flush();
      const values=g.nodes.map(node=>node.textContent);
      assert(values.slice(0,4).every(text=>/^\d{2}$/.test(text)));
      timeline.push({milliseconds,values});
    }
    assert.deepEqual(g.ordinals.map(node=>node.textContent),['01','02','03','04']);
    assert.deepEqual(g.metrics.map(node=>node.textContent),['62','82','83','3']);
    console.log(JSON.stringify({integration:'PASS',version:g.context.window.fsAttributes.numbercount.version,timeline},null,2));
  })().catch(error=>{console.error(error);process.exitCode=1;});
}
console.log('PASS: scoped frames, final values, bounded observer loop, duplicate init, source fallback, invalid values and metric isolation');
