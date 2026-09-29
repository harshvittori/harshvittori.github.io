# Terms and Conditions and Privacy Policy for HV World (HV Test, HV Reset, HV Vault, HV AI).
# Keep these in step with what the apps really do. When a feature changes how data is handled,
# update the matching section here and the "Last updated" date.

UPDATED = "29 September 2026"
CONTACT = ('<a href="https://www.linkedin.com/in/harshvittori" target="_blank" rel="noopener">LinkedIn (Harsh Goyal)</a> '
           'or <a href="https://github.com/harshvittori" target="_blank" rel="noopener">GitHub (harshvittori)</a>')


def page(kind, title, lead, sections):
    toc = "".join('<li><a href="#%s">%s</a></li>' % (sid, h) for sid, h, _ in sections)
    body = "".join('<section id="%s"><h2>%s</h2>%s</section>' % (sid, h, html) for sid, h, html in sections)
    other = ('<a href="/privacy/">Privacy Policy</a>' if kind == "terms" else '<a href="/terms/">Terms and Conditions</a>')
    return '''<main id="main" class="legal">
  <div class="wrap lg">
    <p class="crumb"><a href="/">HV World</a> <span>/</span> %s</p>
    <h1>%s</h1>
    <p class="upd">Last updated: %s</p>
    <p class="lg-lead">%s</p>
    <nav class="toc" aria-label="On this page"><b>On this page</b><ol>%s</ol></nav>
    <div class="lg-body">%s</div>
    <p class="lg-other">See also: %s</p>
  </div>
</main>''' % (title, title, UPDATED, lead, toc, body, other)


# ------------------------------------------------------------------ TERMS
TERMS = [
("about", "1. About these terms", """
<p>These Terms and Conditions ("Terms") are an agreement between you and <b>Harsh Goyal</b>, an individual based in India who builds and runs HV World ("we", "us", "our"). They apply when you visit or use:</p>
<ul>
<li><b>HV World</b>: the website at harshvittori.github.io, including Riya's story and the Watch page;</li>
<li><b>HV Test</b>: self-assessment tests at harshvittori.github.io/hv-tests, including the Skill Assessment Scorecard and the verify page;</li>
<li><b>HV Reset</b>: the day planner and dashboard at harshvittori.github.io/hv-reset;</li>
<li><b>HV Vault</b>: the job search tracker at harshvittori.github.io/hv-vault-web, and its Windows desktop app;</li>
<li><b>HV AI</b>: the assistant built into HV Reset and HV Vault.</li>
</ul>
<p>Together these are the "Services". By using any of the Services you agree to these Terms and to our <a href="/privacy/">Privacy Policy</a>. If you do not agree, please do not use the Services.</p>
<p>These Terms are an electronic record under the Information Technology Act, 2000 and the rules made under it. They do not need a physical or digital signature.</p>
"""),
("eligibility", "2. Who can use the Services", """
<ul>
<li>You must be <b>18 years or older</b>, or use the Services with the permission and supervision of a parent or legal guardian who agrees to these Terms for you.</li>
<li>If you are under 18, please do not sign in, save a scorecard or give us personal information without your parent or guardian's consent.</li>
<li>You must be able to form a binding contract under the law that applies to you, and not be barred from using the Services by any law.</li>
</ul>
"""),
("services", "3. What the Services are", """
<p>The Services are free tools for personal growth, planning and job searching. Some parts work without an account. Others, such as HV Vault and saving your plan in HV Reset, need a Google sign-in.</p>
<p>We may add, change, pause or remove features at any time, including making a feature paid in future. If we introduce paid features, we will tell you the price and terms before you pay, and nothing you have already used for free will be charged retrospectively.</p>
"""),
("accounts", "4. Accounts and sign-in", """
<ul>
<li>Sign-in uses <b>Google sign-in</b> through Google Firebase. We never see or store your Google password.</li>
<li>You are responsible for keeping access to your Google account and your devices secure, and for everything done through your account.</li>
<li>Tell us promptly if you believe someone has used your account without permission.</li>
<li>HV Reset can also sync using a long private sync code. Anyone who has your sync code can read and change that synced data, so keep it private.</li>
</ul>
"""),
("hvtest", "5. HV Test and scorecards", """
<p><b>Self-assessment, not a diagnosis.</b> HV Test tests are self-report questionnaires based on how you say you would act. Results are for personal reflection and growth. They are not a medical, psychological, psychiatric, clinical or professional evaluation, and must not be used as one.</p>
<p><b>What a Skill Assessment Scorecard is.</b> A scorecard is a one-page summary of your test result, issued by HV Test. It is <b>not</b> an accredited certification, degree, diploma, licence or professional qualification. HV Test is not currently affiliated with, endorsed by or recognised by any university, college, government body, examination board or certification authority. Any "coming soon" partnership mentioned on our pages is a plan, not an existing partnership.</p>
<p><b>What verification confirms.</b> When you save a scorecard it gets a unique ID and QR code, and anyone with the ID can see the saved record on the verify page. Verification confirms only that HV Test issued a scorecard with that ID and that the name, date and scores are as saved. It does <b>not</b> confirm your identity: the name on a scorecard is the name you typed. Scores are calculated from your own answers.</p>
<p><b>Your responsibilities with scorecards.</b> You agree to:</p>
<ul>
<li>enter only your own real name, or a name you have the right to use;</li>
<li>not create, alter, fake or misrepresent a scorecard or verification result, including by calling our systems directly;</li>
<li>not present a scorecard as an accredited certificate or as proof of a qualification, and not use it to mislead an employer, institution or anyone else.</li>
</ul>
<p>We may delete any scorecard record that we reasonably believe breaks these Terms, and we may refuse to verify it.</p>
<p><b>Scorecards are public by ID.</b> Anyone who has a scorecard's ID or QR code can see its summary. Saved records cannot be edited. If you want a scorecard removed, contact us (see section 17).</p>
"""),
("ai", "6. HV AI and AI features", """
<ul>
<li>HV AI and the AI auto-fill features (reading resumes, job posts and screenshots) use Google's Gemini models through Google Firebase AI Logic. What you type, say or upload for these features is sent to Google to be processed.</li>
<li><b>AI can be wrong.</b> AI output may be incomplete, out of date or incorrect. HV AI shows each change as a card for you to confirm, edit or cancel. You are responsible for checking AI output before you confirm it or rely on it.</li>
<li>Do not use AI features to process sensitive personal data about yourself or others that you do not need to share, such as financial account numbers, government ID numbers or health information.</li>
<li>If you choose to add your own AI key (for example a Gemini or OpenRouter key) under Advanced settings, your use of that provider is also governed by that provider's own terms, and any costs they charge are yours.</li>
</ul>
"""),
("content", "7. Your content", """
<p>"Your content" means anything you add to the Services: plans, tasks, notes, jobs, companies, contacts, resumes, messages, test answers, scorecard names and anything you tell HV AI.</p>
<ul>
<li><b>You own your content.</b> We do not claim ownership of it.</li>
<li>You give us a limited, non-exclusive, royalty-free permission to store, process, display and transmit your content only as needed to run the Services for you, including sending it to the service providers named in our Privacy Policy. This permission ends when you delete your content or account, except where the law requires us to keep something or where you have made it public (such as a saved scorecard, until it is removed).</li>
<li>You confirm that you have the right to add your content, and that it does not break any law or anyone else's rights. If you add information about other people (for example recruiters or contacts in HV Vault), you are responsible for having a lawful reason to do so.</li>
<li>Keep your own copies of anything important. HV Vault lets you export to Excel and download a full backup.</li>
</ul>
"""),
("use", "8. Acceptable use", """
<p>You agree not to:</p>
<ul>
<li>use the Services for anything unlawful, fraudulent, harmful, abusive, defamatory, obscene or hateful, or to harass anyone;</li>
<li>upload malware, or try to break, overload, probe or get around the security of the Services, Firebase, App Check or our database rules;</li>
<li>access, collect or scrape other people's data, or try to list, guess or harvest scorecard IDs;</li>
<li>create fake or misleading scorecards or records, or impersonate anyone;</li>
<li>copy, resell, rent or offer the Services as your own, or remove our names, logos or notices;</li>
<li>use the Services to build a competing product by copying their design or content;</li>
<li>use automated tools to use the Services in a way that a normal person using a browser would not.</li>
</ul>
<p>Each of the Services also follows the Information Technology (Intermediary Guidelines and Digital Media Ethics Code) Rules, 2021, and you must not use them to host or share content those rules prohibit.</p>
"""),
("ours", "9. Our content and intellectual property", """
<p>The Services, including their names (HV World, HV Test, HV Reset, HV Vault, HV AI), logos, designs, text, questions, illustrations, characters (including Riya), videos and software, belong to us or our licensors and are protected by law. You may use them only to use the Services as intended. Some parts use open-source software and fonts under their own licences (for example the SIL Open Font License), and those licences apply to those parts.</p>
<p>Riya's story and its characters are fictional and for illustration. They do not describe a real person, and they are not a promise of any result.</p>
"""),
("third", "10. Third-party services and links", """
<p>The Services rely on third parties, including Google (Firebase, Google sign-in, Gemini AI, reCAPTCHA Enterprise App Check, Google Fonts), GitHub (website hosting) and Cloudflare (cdnjs, which serves some code libraries). Their services are governed by their own terms and privacy policies, and we are not responsible for them. Links to other websites are provided for convenience only.</p>
"""),
("noguar", "11. No guarantee of results", """
<p>The Services are tools. We do not promise that using them will get you a job, an interview, an offer, a higher score, better habits or any other result. Examples, stories, sample scorecards and numbers shown on our pages are illustrations.</p>
"""),
("warranty", "12. Services provided \"as is\"", """
<p>The Services are provided free of charge, <b>"as is" and "as available"</b>. To the fullest extent the law allows, we make no warranties of any kind, express or implied, including that the Services will be uninterrupted, timely, secure, error-free or free of data loss, or that results, scores or AI output will be accurate, complete or fit for a particular purpose. Features that depend on your browser, device, internet connection or third parties may not always work.</p>
"""),
("liability", "13. Limitation of liability", """
<p>To the fullest extent the law allows:</p>
<ul>
<li>we are not liable for any indirect, incidental, special, consequential or punitive loss, or for loss of profits, opportunities, jobs, data, goodwill or reputation, arising from or related to the Services, even if we were told such loss was possible;</li>
<li>we are not liable for any decision you or anyone else makes based on a test result, scorecard, dashboard number or AI output;</li>
<li>we are not liable for loss or harm caused by third-party services, by events outside our reasonable control, or by your failure to keep your account, devices or sync code secure;</li>
<li>our total liability for all claims relating to the Services is limited to <b>₹1,000 (one thousand Indian rupees)</b> or the amount you paid us for the Services in the 12 months before the claim, whichever is higher.</li>
</ul>
<p>Nothing in these Terms limits liability that cannot be limited under applicable law, including your rights under the Consumer Protection Act, 2019 where they apply.</p>
"""),
("indemnity", "14. Your responsibility to us", """
<p>You agree to make good any loss, damage, claim or reasonable legal cost we suffer because you broke these Terms, broke the law, or used the Services to infringe someone else's rights, including by creating or presenting a misleading scorecard.</p>
"""),
("end", "15. Suspension, deletion and ending use", """
<ul>
<li>You can stop using the Services at any time. You can delete your HV Vault data from Settings ("Delete all data"), clear local data from your browser, and ask us to delete anything else (see section 17).</li>
<li>We may suspend or end your access, or remove content, if we reasonably believe you broke these Terms or the law, if required by law or a court or government order, or to protect the Services or other users. Where reasonable, we will tell you why.</li>
<li>We may shut down any of the Services. If we plan to shut down a service that stores your data, we will try to give reasonable notice so you can export it.</li>
<li>Sections that by their nature should continue (such as 5, 9, 11 to 14 and 16) continue after your use ends.</li>
</ul>
"""),
("law", "16. Governing law and disputes", """
<p>These Terms are governed by the laws of <b>India</b>. Before starting any legal proceedings, you agree to contact us first and try in good faith to resolve the issue informally for at least 30 days. Subject to any rights you have under consumer protection law to bring a claim where you live, the courts of India having jurisdiction over the place where Harsh Goyal ordinarily resides will have exclusive jurisdiction.</p>
"""),
("contact", "17. Contact and grievance officer", """
<p>For any question, complaint, request to remove content or a scorecard, or to report a violation of these Terms, contact <b>Harsh Goyal</b>, who also acts as the Grievance Officer under the Information Technology Act, 2000 and the rules made under it, through """ + CONTACT + """. Please include enough detail for us to find the issue (for example the scorecard ID or the page and date).</p>
<p>We will acknowledge a complaint within <b>24 hours</b> and aim to resolve it within <b>15 days</b> of receiving it, or sooner where the law requires.</p>
"""),
("changes", "18. Changes to these terms", """
<p>We may update these Terms from time to time. The "Last updated" date at the top shows when they last changed. If a change is significant, we will make reasonable efforts to point it out on the website or in the apps. If you keep using the Services after a change takes effect, you accept the updated Terms.</p>
<p>If any part of these Terms is found to be unenforceable, the rest stays in effect. If we do not enforce a right straight away, we can still enforce it later. These Terms and the Privacy Policy are the whole agreement between you and us about the Services.</p>
"""),
]

# ------------------------------------------------------------------ PRIVACY
PRIVACY = [
("who", "1. Who we are", """
<p>HV World, HV Test, HV Reset, HV Vault and HV AI (the "Services") are built and run by <b>Harsh Goyal</b>, an individual based in India ("we", "us", "our"). For personal data handled through the Services, we act as the "Data Fiduciary" under India's Digital Personal Data Protection Act, 2023 (DPDP Act), and we follow the Information Technology Act, 2000 and the Information Technology (Reasonable Security Practices and Procedures and Sensitive Personal Data or Information) Rules, 2011.</p>
<p>This policy explains what we collect, why, where it goes, how long we keep it, and your rights. By using the Services you agree to this policy and our <a href="/terms/">Terms and Conditions</a>.</p>
"""),
("short", "2. The short version", """
<ul>
<li><b>No ads, no trackers, no analytics.</b> We do not use advertising, analytics or tracking tools, and we do not sell or rent your data.</li>
<li><b>HV Test</b> needs no account. Your answers, age and profession stay in your browser. We save data only if you choose to save a scorecard, plus an anonymous count of finished tests.</li>
<li><b>HV Reset</b> works without an account, saving on your device. If you sign in, your plan and history sync to your private account.</li>
<li><b>HV Vault</b> uses Google sign-in and stores your job search in your private account. Only you can read it.</li>
<li><b>HV AI</b> sends what you ask it to Google's Gemini AI to process.</li>
<li>Your data is stored with Google Firebase. You can export or delete it.</li>
</ul>
"""),
("collect", "3. What we collect, app by app", """
<h3>HV World website</h3>
<ul>
<li>We do not ask for any personal data on the website, and we do not use cookies there.</li>
<li>The site is hosted on <b>GitHub Pages</b>. Like any web host, GitHub automatically receives technical data such as your IP address, browser type and the pages requested, to deliver and secure the site. We cannot see or control GitHub's logs.</li>
<li>Your browser may store small preferences locally (for example whether a video has sound).</li>
</ul>
<h3>HV Test</h3>
<ul>
<li><b>Stays on your device only:</b> the name, age, profession and focus you enter, every answer, your response times, your full results and your PDFs. These are never sent to us.</li>
<li><b>Saved only if you choose "Add ID and QR code":</b> a scorecard record containing the name you confirm, the test name and category, the date and time you finished, your overall score and level, how many questions you answered, your score for each skill, your top strengths and areas to work on, and the scorecard ID. <b>Your answers, age and profession are not saved.</b></li>
<li><b>Anonymous counter:</b> when anyone finishes a test, we add 1 to a daily count for that test. It contains no name, answers, device or location data.</li>
<li><b>On your device:</b> your theme choice and similar settings, in local storage.</li>
</ul>
<h3>HV Reset</h3>
<ul>
<li><b>Without an account:</b> your tasks, plans, timers, habits, goals, dashboard history and settings are saved in your browser's local storage on that device.</li>
<li><b>If you sign in with Google:</b> we receive your Google account ID, name, email address and profile picture from Google, and we sync your plan, history and settings to your private space in our database.</li>
<li><b>Profile details you choose to give</b>, such as your name, role or goals, to personalise the app.</li>
<li><b>Sync code (optional):</b> if you use a sync code instead of sign-in, your data is saved under that long private code.</li>
<li><b>With HV Vault:</b> if you use both apps with the same Google account, HV Reset reads your follow-ups due and weekly numbers from HV Vault to show them next to your day.</li>
</ul>
<h3>HV Vault</h3>
<ul>
<li><b>Account:</b> your Google account ID, name, email address and profile picture, from Google sign-in.</li>
<li><b>Your job search:</b> jobs, companies, links, salaries, locations, notes, statuses, follow-ups, interviews, calendar items, message templates and analytics.</li>
<li><b>Contacts you add</b>, such as recruiters or referrers (names, roles, emails, phone numbers or links). Please add only what you need and have a lawful reason to keep.</li>
<li><b>Resume and profile:</b> resume files you upload and the details read from them, such as your name, role, skills, experience and education.</li>
<li><b>Items you paste or upload for AI auto-fill</b>, such as job post text, PDFs and screenshots.</li>
<li><b>The Windows desktop app</b> stores data on your computer. If you connect it to your account, it syncs the same way as the web app.</li>
</ul>
<h3>HV AI</h3>
<ul>
<li>The messages you type, your voice recordings when you use the mic, and the information needed to act on them (for example your current tasks or jobs) are sent to Google's Gemini models through Google Firebase AI Logic to produce a reply.</li>
<li>Your recent HV AI conversation may be saved on your device and, if you are signed in, with your account, so it can continue where you left off.</li>
<li>If you add your own AI key under Advanced settings, it is stored on your device and your requests go directly to that provider under their terms.</li>
</ul>
<h3>Security checks</h3>
<ul>
<li>To block abuse, some requests include a Google <b>reCAPTCHA Enterprise / Firebase App Check</b> token. Google may collect device and browser signals, and may use cookies, to produce it, under Google's own privacy policy.</li>
</ul>
"""),
("sensitive", "4. Sensitive information", """
<p>We do not ask for passwords, financial information, card or bank details, health or medical records, biometric data, government ID numbers, caste, religion or sexual orientation. Please do not put this kind of information into notes, resumes, AI messages or any other field. HV Test results are a self-assessment about behaviour, not health data, and we do not store your answers.</p>
"""),
("why", "5. Why we use your data", """
<ul>
<li>To provide the features you ask for: saving and syncing your plans and job search, showing your dashboard, running tests, issuing and verifying scorecards, and answering HV AI requests.</li>
<li>To keep the Services secure, prevent abuse and fake records, and fix problems.</li>
<li>To understand usage at a high level through the anonymous count of finished tests and the total number of scorecards issued.</li>
<li>To respond to your requests and complaints, and to meet legal obligations.</li>
</ul>
<p>Our legal basis is your <b>consent</b>, given when you choose to use a feature (for example signing in, saving a scorecard or asking HV AI), and certain legitimate uses allowed by the DPDP Act, such as complying with law. You can withdraw consent at any time by stopping use of the feature and deleting the related data. Withdrawing consent does not affect processing already done.</p>
<p>We do <b>not</b> use your data for advertising, we do not sell or rent it, and we do not use your content to train our own AI models.</p>
"""),
("share", "6. Who we share data with", """
<p>We share data only with service providers that run parts of the Services for us, and only as needed:</p>
<ul>
<li><b>Google (Firebase):</b> authentication, database storage, App Check and AI processing (Gemini through Firebase AI Logic). Google may process data on servers outside India.</li>
<li><b>GitHub:</b> hosts the website and web apps.</li>
<li><b>Google Fonts and Cloudflare (cdnjs):</b> deliver fonts and code libraries to your browser. They receive technical data such as your IP address when your browser loads them.</li>
<li><b>Public scorecards:</b> a saved scorecard summary can be seen by anyone who has its ID or QR code. You decide who to share it with.</li>
<li><b>Legal reasons:</b> we may disclose information if required by law, a court order or a lawful request from a government authority, or to protect the rights, safety or property of users, the public or us.</li>
</ul>
<p>We do not share your data with employers, recruiters, colleges or any other organisation unless you share it yourself.</p>
"""),
("transfer", "7. Where your data is stored", """
<p>Data is stored in Google Firebase (project "harsh-reset") and processed by the providers above. Their servers may be located outside India. Where we transfer data outside India, we do so as permitted under the DPDP Act and any restrictions notified by the Government of India.</p>
"""),
("keep", "8. How long we keep data", """
<ul>
<li><b>Data on your device</b> stays until you delete it or clear your browser data.</li>
<li><b>HV Vault and HV Reset account data</b> is kept while you use your account. When you delete it (for example with "Delete all data" in HV Vault) or ask us to, we delete it from our active database, normally within 30 days. Short-lived copies held by our providers may take a little longer to expire.</li>
<li><b>Scorecards</b> are kept so they can be verified, until you ask us to remove them or we remove them under our Terms.</li>
<li><b>The anonymous count</b> of finished tests contains no personal data and may be kept indefinitely.</li>
<li>We may keep limited information for longer where the law requires it or to resolve a dispute.</li>
</ul>
"""),
("security", "9. How we protect your data", """
<ul>
<li>All connections to the Services use HTTPS encryption.</li>
<li>Our database rules allow a signed-in user to read and write only their own data. Scorecards can be created once and read by ID, but cannot be listed, edited or deleted by the public.</li>
<li>Firebase App Check helps block requests that do not come from our apps.</li>
<li>Access to the admin view of scorecards is limited to one owner account.</li>
</ul>
<p>No system is completely secure. If we become aware of a personal data breach that affects you, we will notify you and the Data Protection Board of India as required by law.</p>
"""),
("rights", "10. Your rights", """
<p>Under the DPDP Act and other applicable law, you have the right to:</p>
<ul>
<li><b>access</b> a summary of the personal data we hold about you and how we use it;</li>
<li><b>correct, complete or update</b> it;</li>
<li><b>delete</b> it (erasure), unless we must keep it by law;</li>
<li><b>withdraw consent</b> at any time;</li>
<li><b>nominate</b> another person to exercise your rights if you die or become unable to;</li>
<li><b>raise a grievance</b> with us, and if you are not satisfied, complain to the Data Protection Board of India.</li>
</ul>
<p>Many of these you can do yourself: edit or delete items in the apps, export or delete everything in HV Vault's Settings, and clear local data in your browser. For anything else, including removing a scorecard, contact us (section 14). We may need to confirm it is you before acting.</p>
"""),
("children", "11. Children", """
<p>The Services are meant for people aged 18 and over. People under 18 should use them only with a parent or guardian's consent and supervision, and should not sign in or save a scorecard without it. We do not knowingly process children's personal data without verifiable parental consent, and we do not track or target advertising at children. If you believe a child has given us personal data without consent, contact us and we will delete it.</p>
"""),
("storage", "12. Cookies and local storage", """
<ul>
<li>We do not use advertising or analytics cookies.</li>
<li>The apps use your browser's <b>local storage</b> to save your data and settings on your device, and Firebase uses browser storage to keep you signed in.</li>
<li>Google's reCAPTCHA Enterprise may set its own cookies for security checks.</li>
<li>You can clear this data from your browser settings at any time. Clearing it removes data that is saved only on that device.</li>
</ul>
"""),
("changes", "13. Changes to this policy", """
<p>We may update this policy as the Services change. The "Last updated" date at the top shows the latest version. If we make a significant change to how we use personal data, we will point it out on the website or in the apps, and ask for your consent again where the law requires.</p>
"""),
("contact", "14. Contact and grievance officer", """
<p>For privacy questions, requests to access, correct or delete your data, to remove a scorecard, or to raise a grievance, contact <b>Harsh Goyal</b>, Grievance Officer and Data Fiduciary for the Services, through """ + CONTACT + """.</p>
<p>We will acknowledge your message within <b>24 hours</b> and aim to resolve it within <b>15 days</b>, or sooner where the law requires. If you are not satisfied with our response, you may complain to the Data Protection Board of India.</p>
"""),
]

TERMS_LEAD = "Please read these terms before using HV World, HV Test, HV Reset, HV Vault or HV AI. They explain what the Services are, what you can expect from us, and what we expect from you."
PRIVACY_LEAD = "This policy explains what personal data HV World, HV Test, HV Reset, HV Vault and HV AI collect, why, who it is shared with, how long it is kept, and the rights you have over it."

CSS = """
.legal{background:#fff}
.lg{max-width:780px;padding:56px 0 88px}
.legal h1{font-size:clamp(34px,5vw,52px);font-weight:700;letter-spacing:-.04em;line-height:1.08;margin:6px 0 10px}
.legal .upd{font-size:14.5px;color:var(--faint)}
.legal .lg-lead{font-size:19px;color:var(--soft);line-height:1.5;margin:18px 0 26px}
.toc{background:var(--gray,#F2F3F6);border:1px solid var(--line);border-radius:18px;padding:20px 24px;margin-bottom:36px}
.toc b{display:block;font-size:14px;margin-bottom:8px}
.toc ol{list-style:none;margin:0;padding-left:0;columns:2;column-gap:28px;font-size:15px;line-height:1.9}
.toc a{color:var(--accent);text-decoration:none}.toc a:hover{text-decoration:underline}
.lg-body section{padding-top:14px;scroll-margin-top:80px}
.lg-body h2{font-size:23px;font-weight:700;letter-spacing:-.02em;margin:26px 0 10px}
.lg-body h3{font-size:17px;font-weight:700;margin:20px 0 6px}
.lg-body p,.lg-body li{font-size:16.5px;line-height:1.65;color:#3A3A3C}
.lg-body p{margin:0 0 12px}
.lg-body ul{margin:0 0 14px;padding-left:22px}.lg-body li{margin-bottom:6px}
.lg-body a,.lg-other a{color:var(--accent)}
.lg-other{margin-top:40px;padding-top:20px;border-top:1px solid var(--line);font-size:15.5px;color:var(--soft)}
@media (max-width:640px){.lg{padding:36px 0 64px}.toc ol{columns:1}.lg-body p,.lg-body li{font-size:16px}.legal .lg-lead{font-size:17.5px}}
"""
