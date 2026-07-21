---
hide:
  - toc
  - navigation
---

<div class="guide-hero usage-hero">
  <p class="guide-hero__eyebrow">Using WoWidget</p>
  <h1>Character Selection</h1>
  <p class="guide-hero__summary">Find a World of Warcraft character, verify the returned profile, and choose which character WoWidget sends to Discord.</p>
  <div class="guide-meta"><span>Character lookup</span><span>Region, realm, and name required</span></div>
</div>

<div class="usage-overview">
  <a href="#search-for-a-character"><span>01</span><strong>Search</strong><small>Enter the character details.</small></a>
  <a href="#verify-the-result"><span>02</span><strong>Verify</strong><small>Confirm the returned profile.</small></a>
  <a href="#switch-characters"><span>03</span><strong>Select</strong><small>Save or replace the active character.</small></a>
</div>

<section class="guide-step" id="search-for-a-character">
  <div class="guide-step__heading"><span class="step-number">1</span><h2>Search for a character</h2></div>
  <p>Open the character-selection screen and enter the character's region, realm, and name exactly as they appear in World of Warcraft. Select <strong>Search</strong> to request the profile from Blizzard.</p>

  <div class="usage-field-grid">
    <article class="usage-field-card">
      <span class="usage-field-card__label">Region</span>
      <strong>Choose the account region</strong>
      <p>Select the region where the character exists, such as Americas, Europe, Korea, or Taiwan.</p>
    </article>
    <article class="usage-field-card">
      <span class="usage-field-card__label">Realm</span>
      <strong>Use the full realm name</strong>
      <p>Spaces and punctuation are normalized automatically, but the selected region must still be correct.</p>
    </article>
    <article class="usage-field-card">
      <span class="usage-field-card__label">Character</span>
      <strong>Enter the character name</strong>
      <p>Capitalization is not important. Special characters must match the in-game name.</p>
    </article>
  </div>

  <aside class="ww-callout ww-callout--tip"><strong>Character not found?</strong><span>Confirm the region and realm first. Most lookup failures are caused by searching the correct name on the wrong realm or regional API.</span></aside>
</section>

<section class="guide-step" id="verify-the-result">
  <div class="guide-step__heading"><span class="step-number">2</span><h2>Verify the returned profile</h2></div>
  <p>Before selecting the character, review the summary returned by WoWidget. The name alone is not enough when similarly named characters exist on multiple realms.</p>

  <div class="usage-checklist">
    <div><span>✓</span><p><strong>Name and realm</strong><small>Confirm both values belong to the intended character.</small></p></div>
    <div><span>✓</span><p><strong>Race and class</strong><small>Check that the returned identity matches the in-game character.</small></p></div>
    <div><span>✓</span><p><strong>Guild and level</strong><small>Use these as additional confirmation when available.</small></p></div>
    <div><span>✓</span><p><strong>Character portrait</strong><small>The Blizzard render should resemble the selected character, though it may reflect Outfit Slot 1.</small></p></div>
  </div>

  <aside class="ww-callout ww-callout--note"><strong>Blizzard data may be delayed</strong><span>Recently changed equipment, guild information, progression, or appearance data may take time to update in Blizzard's profile services.</span></aside>
</section>

<section class="guide-step" id="switch-characters">
  <div class="guide-step__heading"><span class="step-number">3</span><h2>Select or switch characters</h2></div>
  <p>Select <strong>Use this Character</strong> after verifying the result. WoWidget stores the selection locally and uses it for portrait generation, data refreshes, and future Discord widget updates.</p>

  <div class="usage-action-grid">
    <article>
      <span>Current character</span>
      <h3>Keep the active selection</h3>
      <p>No action is required. Manual and automatic updates continue using the currently selected character.</p>
    </article>
    <article>
      <span>Different character</span>
      <h3>Run another search</h3>
      <p>Open character selection again, search for the replacement, verify it, and select <strong>Use this Character</strong>.</p>
    </article>
    <article>
      <span>After switching</span>
      <h3>Create a new portrait</h3>
      <p>Generate and save a portrait for the newly selected character before sending the next widget update.</p>
    </article>
  </div>
</section>

<div class="guide-panel usage-next">
  <div>
    <p class="guide-hero__eyebrow">Next guide</p>
    <h2>Build the character portrait</h2>
    <p>Generate the Blizzard model, position it inside the widget crop, and save the finished image.</p>
  </div>
  <a class="md-button md-button--primary" href="../portrait-studio/">Open Portrait Studio guide</a>
</div>
