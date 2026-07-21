---
hide:
  - toc
  - navigation
---

<div class="guide-hero">
  <p class="guide-hero__eyebrow">Getting Started · Step 3 of 5</p>
  <h1>Discord Setup</h1>
  <p class="guide-hero__summary">Create the Discord application that owns your profile widget, configure OAuth, and enable Discord's experimental Widget Editor.</p>
  <div class="guide-meta"><span>⏱ 8–12 minutes</span><span>Discord account required</span></div>
</div>

<nav class="setup-progress" aria-label="Setup progress">
  <ol>
    <li class="is-complete"><a href="../installation/" data-step="1"><span class="setup-progress__marker" data-step="1" aria-hidden="true"></span><span class="setup-progress__label">Installation</span></a></li>
    <li class="is-complete"><a href="../blizzard-setup/" data-step="2"><span class="setup-progress__marker" data-step="2" aria-hidden="true"></span><span class="setup-progress__label">Blizzard</span></a></li>
    <li class="is-current" aria-current="step"><a href="../discord-setup/" data-step="3"><span class="setup-progress__marker" data-step="3" aria-hidden="true"></span><span class="setup-progress__label">Discord</span></a></li>
    <li><a href="../widget-editor/" data-step="4"><span class="setup-progress__marker" data-step="4" aria-hidden="true"></span><span class="setup-progress__label">Widget</span></a></li>
    <li><a href="../application-setup/" data-step="5"><span class="setup-progress__marker" data-step="5" aria-hidden="true"></span><span class="setup-progress__label">Application</span></a></li>
  </ol>
</nav>

<div class="guide-panel" markdown="1">
<h2>Before you begin</h2>
<p>Open the <a href="https://discord.com/developers/applications">Discord Developer Portal</a>. Keep the temporary credential note from Blizzard Setup open, as you will add three Discord values to it.</p>
</div>

<div class="guide-step guide-step--split" markdown="1">
<div class="guide-step__copy">
<div class="guide-step__heading"><span class="step-number">1</span><h2>Create a new application</h2></div>
<p>Open <strong>Applications</strong>, select <strong>New Application</strong>, name it <strong>WoWidget</strong>, and select <strong>Create</strong>.</p>
</div>
<figure class="doc-screenshot">
  <img src="../../assets/images/discord/01-new-application.png" alt="Discord Developer Portal New Application dialog" loading="lazy">
  <figcaption>Create the Discord application that will own your widget.</figcaption>
</figure>
</div>

!!! warning "Choose a safe application name"
    The application name appears on your Discord profile widget. Use a normal, Terms-of-Service-compliant name. `WoWidget` is the recommended option, but you remain responsible for the name you publish.

<div class="guide-step guide-step--split" markdown="1">
<div class="guide-step__copy">
<div class="guide-step__heading"><span class="step-number">2</span><h2>Save the Application ID</h2></div>
<p>Copy the <strong>Application ID</strong> into your temporary credential note. You may also upload an application icon now.</p>
<p>The icon is optional.</p> <p>You do not need the Public Key for WoWidget.</p>
</div>
<figure class="doc-screenshot">
  <img src="../../assets/images/discord/02-application-id.png" alt="Discord application General Information page" loading="lazy">
  <figcaption>Copy the Application ID and optionally add an application icon.</figcaption>
</figure>
</div>

<div class="guide-step guide-step--split" markdown="1">
<div class="guide-step__copy">
<div class="guide-step__heading"><span class="step-number">3</span><h2>Configure OAuth2</h2></div>
<p>Open <strong>OAuth2</strong>, copy the <strong>Client Secret</strong> into your temporary credential note, and add both redirect URLs below. Select <strong>Save Changes</strong>.</p>
<div class="copy-field"><code>http://discord.com</code><button class="copy-button" data-copy="http://discord.com">Copy</button></div>
<div class="copy-field"><code>http://127.0.0.1:5001/callback</code><button class="copy-button" data-copy="http://127.0.0.1:5001/callback">Copy</button></div>
</div>
<figure class="doc-screenshot">
  <img src="../../assets/images/discord/03-oauth-setup.png" alt="Discord OAuth2 settings with redirect URLs" loading="lazy">
  <figcaption>Copy the Client Secret, add both redirect URLs, and save changes.</figcaption>
</figure>
</div>

<div class="guide-step guide-step--split" markdown="1">
<div class="guide-step__copy">
<div class="guide-step__heading"><span class="step-number">4</span><h2>Generate a Bot Token</h2></div>
<p>Open the <strong>Bot</strong> page, generate or reset the Bot Token, and copy it into your temporary credential note.</p>
</div>
<figure class="doc-screenshot">
  <img src="../../assets/images/discord/04-bot-token.png" alt="Discord Bot page with token controls" loading="lazy">
  <figcaption>Generate or reset the Bot Token, then store it securely.</figcaption>
</figure>
</div>

!!! danger "Protect Discord credentials"
    Never share the Client Secret or Bot Token. Do not expose either value in screenshots, GitHub commits, or support messages.

<div class="guide-step guide-step--split" id="complete-the-social-sdk-form" markdown="1">
<div class="guide-step__copy">
<div class="guide-step__heading"><span class="step-number">5</span><h2>Complete the Social SDK form</h2></div>
<p>Open <strong>Social SDK</strong> in the Games section. Complete the required fields, accept the Privacy Policy, and select <strong>Submit</strong>.</p>
<p>Most fields are informational. The Work Email field must use an email-shaped value such as <code>name@example.com</code>.</p>
</div>
<figure class="doc-screenshot">
  <img src="../../assets/images/discord/05-social-sdk-form.png" alt="Discord Social SDK setup form" loading="lazy">
  <figcaption>Complete the required Social SDK form and submit it.</figcaption>
</figure>
</div>

!!! danger "This step is required"
    If the Social SDK form is incomplete, Discord authorization may fail with `The requested scope is invalid, unknown or malformed` or display `Discord Authorization Cancelled`.

<div class="guide-step" markdown="1">
<div class="guide-step__heading"><span class="step-number">6</span><h2>Enable the Experimental Widget Editor</h2></div>
<p>Select the Discord Developer Portal's <strong>back arrow</strong> in the upper-left corner—not the browser Back button. From the Developer Portal home screen:</p>
<ol>
<li>Press <strong>Ctrl + Shift + I</strong> to open Developer Tools.</li>
<li>Open the <strong>Console</strong> tab.</li>
<li>Copy the command below, paste it into the Console, and press <strong>Enter</strong>.</li>
<li>Confirm that the console returns <code>undefined</code>.</li>
<li>Close Developer Tools and reopen your application.</li>
</ol>

<div class="ww-command-card">
  <div class="ww-command-card__header">
    <div>
      <span class="ww-command-card__eyebrow">Discord Developer Console</span>
      <h3>Enable Widget Editor</h3>
      <p>Run this command once from the Developer Portal home screen.</p>
    </div>
  </div>

  <div class="ww-command-card__body">
    </button>
    <pre class="ww-command-card__code"><code id="widget-editor-command">let _mods = webpackChunkdiscord_developers.push([[Symbol()],{},r=&gt;r.c]);
webpackChunkdiscord_developers.pop();

let findByProps = (...props) =&gt; {
    for (let m of Object.values(_mods)) {
        try {
            if (!m.exports || m.exports === window) continue;
            if (props.every((x) =&gt; m.exports?.[x])) return m.exports;

            for (let ex in m.exports) {
                if (props.every((x) =&gt; m.exports?.[ex]?.[x]) &amp;&amp; m.exports[ex][Symbol.toStringTag] !== &#x27;IntlMessagesProxy&#x27;) return m.exports[ex];
            }
        } catch {}
    }
}

findByProps(&quot;getAll&quot;).getAll().find(e=&gt;e.getName() === &quot;ApexExperimentStore&quot;).createOverride(&quot;2026-03-widget-config-editor&quot;, 1)</code></pre>
  </div>

  <div class="ww-command-card__footer">
    <span>Expected console response</span>
    <code>undefined</code>
  </div>
</div>

<div class="screenshot-gallery screenshot-gallery--2">
<figure class="doc-screenshot">
  <img src="../../assets/images/discord/06-developer-console.png" alt="Browser Developer Tools console used to enable Widget Editor" loading="lazy">
  <figcaption>Return to the home screen via the back button.</figcaption>
</figure>
<figure class="doc-screenshot">
  <img src="../../assets/images/discord/07-widget-tab-enabled.png" alt="Discord Developer Portal with Widget tab enabled" loading="lazy">
  <figcaption>Run the enablement command, and confirm that the console returns 'Undefined'.</figcaption>
</figure>
</div>
</div>

!!! tip "Type Allow Pasting"
    If this is your first time using the developer console on the Discord Dev Portal, you may be required to type allow pasting before you can paste the enablement command. You only need to do this the first time, and the browser will remember your preference in the future.

!!! warning "Developer Console safety"
    Never paste code into a browser console unless you understand or trust its source. You can verify the safety of this command by searching "how to enable the experimental widget feature in discord dev portal" on Google.

!!! note "Do not refresh yet"
    Refreshing the Developer Portal before publishing may remove access to the experimental Widget Editor. Repeat this step if the Widget section disappears. After your widget is published, you may safely close the site.

<style>
.ww-command-card {
  margin: 1.6rem 0 2rem;
  overflow: hidden;
  border: 1px solid rgba(154, 124, 255, .28);
  border-radius: 18px;
  background: #12101a;
  box-shadow: 0 18px 50px rgba(0, 0, 0, .22);
}

.ww-command-card__header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 1.5rem;
  padding: 1.55rem 1.75rem;
  border-bottom: 1px solid rgba(255, 255, 255, .07);
  background: linear-gradient(135deg, rgba(117, 78, 190, .20), rgba(44, 35, 65, .34));
}

.ww-command-card__eyebrow {
  display: block;
  margin-bottom: .35rem;
  color: #b69cff;
  font-size: .74rem;
  font-weight: 800;
  letter-spacing: .09em;
  text-transform: uppercase;
}

.ww-command-card__header h3 {
  margin: 0;
  font-size: 1.22rem;
  line-height: 1.25;
}

.ww-command-card__header p {
  margin: .4rem 0 0;
  color: var(--md-default-fg-color--light);
}

.ww-command-card__language {
  flex: 0 0 auto;
  padding: .42rem .7rem;
  border: 1px solid rgba(182, 156, 255, .24);
  border-radius: 999px;
  background: rgba(182, 156, 255, .09);
  color: #d4c7ff;
  font: 700 .72rem/1 var(--md-code-font-family);
}

.ww-command-card__body {
  position: relative;
  padding: 1.3rem;
  background: #0e0c14;
}

.ww-command-card__code {
  max-height: 31rem;
  margin: 0;
  overflow: auto;
  padding: 1.35rem 1.45rem;
  padding-top: 3.6rem;
  border: 1px solid rgba(255, 255, 255, .055);
  border-radius: 12px;
  background: #191522;
  color: #e7e1f2;
  font-family: "JetBrains Mono", "Fira Code", Consolas, monospace;
  font-size: .78rem;
  line-height: 1.7;
  tab-size: 4;
  white-space: pre;
}

.ww-command-card__code code {
  display: block;
  padding: 0;
  background: transparent;
  color: inherit;
  font: inherit;
  white-space: inherit;
}

.ww-command-card__copy {
  position: absolute;
  z-index: 2;
  top: 2rem;
  right: 2rem;
  display: inline-flex;
  align-items: center;
  gap: .45rem;
  min-height: 2.25rem;
  padding: .48rem .72rem;
  border: 1px solid rgba(182, 156, 255, .25);
  border-radius: 9px;
  background: rgba(43, 36, 66, .96);
  color: #f0ebff;
  font: 700 .72rem/1 var(--md-text-font-family);
  cursor: pointer;
  transition: transform .16s ease, background-color .16s ease, border-color .16s ease;
}

.ww-command-card__copy:hover {
  transform: translateY(-1px);
  border-color: rgba(182, 156, 255, .55);
  background: #40335d;
}

.ww-command-card__copy-icon {
  font-size: 1rem;
  line-height: 1;
}

.ww-command-card__footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
  padding: .9rem 1.35rem;
  border-top: 1px solid rgba(255, 255, 255, .07);
  color: var(--md-default-fg-color--light);
  font-size: .82rem;
}

.ww-command-card__footer code {
  padding: .32rem .58rem;
  border: 1px solid rgba(182, 156, 255, .25);
  border-radius: 7px;
  background: rgba(182, 156, 255, .08);
  color: #d9ceff;
}

@media (max-width: 700px) {
  .ww-command-card__header {
    flex-direction: column;
    padding: 1.25rem;
  }

  .ww-command-card__body {
    padding: .9rem;
  }

  .ww-command-card__copy {
    top: 1.55rem;
    right: 1.55rem;
  }

  .ww-command-card__code {
    padding: 3.4rem 1rem 1rem;
    font-size: .72rem;
  }

  .ww-command-card__footer {
    align-items: flex-start;
    flex-direction: column;
  }
}
</style>

<script>
function copyWidgetEditorCommand(button) {
  const code = document.getElementById("widget-editor-command").textContent;
  navigator.clipboard.writeText(code).then(() => {
    const label = button.querySelector(".ww-command-card__copy-label");
    const original = label.textContent;
    label.textContent = "Copied";
    button.classList.add("is-copied");
    window.setTimeout(() => {
      label.textContent = original;
      button.classList.remove("is-copied");
    }, 1800);
  });
}
</script>
