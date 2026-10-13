# Existing footer award overflow at 480px

**Pre-existing; outside this content transfer.** At viewport 480px, the horizontal awards row extends to 512px and clips the final Spinawards logo. The same clipping is visible in the original pre-write capture and the final capture. At 479px the original mobile stacking rule applies and this particular overflow is absent.

Evidence: [side-by-side footer crop](comparison-footer-480.png), [before 480px](before-480.png), [after 480px](after-480.png), [final DOM geometry](layout-dom-audit.json).

The transfer changed the footer year only. Existing styles, images and structure were preserved; no attempt was made to fix this layout defect. A separate future task can adjust award-row wrapping or sizing and verify the 479/480 and 767/768 boundaries across all pages using this Footer definition. That strategy is a suggestion, not an implemented fix or an established root cause.
