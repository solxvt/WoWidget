---
hide:
  - toc
  - navigation
---

<div class="guide-hero usage-hero">
  <p class="guide-hero__eyebrow">Using WoWidget</p>
  <h1>Portrait Studio</h1>
  <p class="guide-hero__summary">Generate the selected character's model, position it for Discord's Hero layout, and save the portrait used by your widget.</p>
  <div class="guide-meta"><span>Visual editor</span><span>Raw model stored locally</span></div>
</div>

<div class="usage-overview">
  <a href="#generate-the-model"><span>01</span><strong>Generate</strong><small>Fetch the Blizzard render.</small></a>
  <a href="#position-the-character"><span>02</span><strong>Position</strong><small>Frame the model for the widget.</small></a>
  <a href="#save-and-review"><span>03</span><strong>Save</strong><small>Export and review the portrait.</small></a>
</div>

<section class="guide-step guide-step--split" id="generate-the-model">
  <div class="guide-step__copy">
    <div class="guide-step__heading"><span class="step-number">1</span><h2>Generate the character model</h2></div>
    <p>Open <strong>Portrait Studio</strong> and select <strong>Generate Portrait</strong>. WoWidget retrieves the official Blizzard character render for the active character and prepares it for editing.</p>
    <p>The raw model is stored locally after a successful generation. You can reopen Portrait Studio and adjust the crop without requesting the same model again.</p>
    <aside class="ww-callout ww-callout--note"><strong>Appearance source</strong><span>Blizzard's rendered character media commonly reflects Outfit Slot 1 rather than the outfit most recently worn in game.</span></aside>
  </div>
  <figure class="doc-screenshot">
    <img src="../../assets/images/application/06-portrait-editor.png" alt="WoWidget Portrait Studio showing the character model and crop area" loading="lazy">
    <figcaption>Generate the model once, then reposition it as often as needed.</figcaption>
  </figure>
</section>

<section class="guide-step" id="position-the-character">
  <div class="guide-step__heading"><span class="step-number">2</span><h2>Position the character</h2></div>
  <p>Drag and scale the model until the important parts of the character remain visible inside the portrait guide. The final widget places text on the left and the model on the right, so the composition should favor the upper-right portion of the canvas.</p>

  <div class="portrait-guidance">
    <article class="portrait-guidance__do">
      <span>Recommended</span>
      <h3>Frame for the Hero layout</h3>
      <ul>
        <li>Keep the face and upper torso clearly visible.</li>
        <li>Place the model near the right edge.</li>
        <li>Leave the left side open for character text.</li>
        <li>Keep signature weapons, wings, or class effects visible when possible.</li>
      </ul>
    </article>
    <article class="portrait-guidance__avoid">
      <span>Avoid</span>
      <h3>Common composition problems</h3>
      <ul>
        <li>Centering the character over the text area.</li>
        <li>Cropping the face, horns, or primary weapon.</li>
        <li>Making the model too small to read at Discord size.</li>
        <li>Relying on details outside the visible guide area.</li>
      </ul>
    </article>
  </div>

  <aside class="ww-callout ww-callout--tip"><strong>Start slightly larger than expected</strong><span>Discord displays the image inside a compact card. A strong upper-body crop generally reads better than trying to preserve the entire character model.</span></aside>
</section>

<section class="guide-step" id="save-and-review">
  <div class="guide-step__heading"><span class="step-number">3</span><h2>Save and review the portrait</h2></div>
  <p>Select <strong>Save Portrait</strong> when the composition is ready. The saved portrait becomes the value sent through the <code>character_model</code> image field during the next widget update.</p>

  <div class="usage-checklist">
    <div><span>1</span><p><strong>Save the portrait</strong><small>Export the current position and crop.</small></p></div>
    <div><span>2</span><p><strong>Update the widget</strong><small>Send the saved portrait and current character data to Discord.</small></p></div>
    <div><span>3</span><p><strong>Review on your profile</strong><small>Check the real Discord widget rather than relying only on the editor preview.</small></p></div>
    <div><span>4</span><p><strong>Refine when needed</strong><small>Return to Portrait Studio, reposition, save, and update again.</small></p></div>
  </div>
</section>

<div class="guide-panel usage-next">
  <div>
    <p class="guide-hero__eyebrow">Next guide</p>
    <h2>Keep the widget current</h2>
    <p>Learn the difference between manual updates, automatic intervals, and the data WoWidget refreshes.</p>
  </div>
  <a class="md-button md-button--primary" href="../updating-widget/">Open Updating Your Widget</a>
</div>
