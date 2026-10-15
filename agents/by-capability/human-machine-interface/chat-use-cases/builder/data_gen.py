import json, re, pathlib, glob, os
HERE=pathlib.Path(__file__).resolve().parent; R=HERE.parents[3]; HMI=R/'by-capability/human-machine-interface'
def h1(f): return re.sub(r':\s*Causes and Fixes$','',f.read_text(encoding='utf-8').splitlines()[0].lstrip('# ').strip())
def issue(f):
    t=f.read_text(encoding='utf-8'); m=re.search(r'^## Issue:?[ \t]*(.*)\n+(.*)',t,re.M)
    s=(m.group(1).strip() or m.group(2).strip()) if m else ''
    s=re.sub(r'^[-*]\s*','',s); j=s.find('. ')
    if j>=40: s=s[:j]
    if len(s)>150: s=s[:150].rsplit(' ',1)[0]+'…'
    return s.rstrip('.')
def find(g,pre):
    d=R/g/'failures'; c=[f for f in d.glob('*.md') if f.name.startswith(pre)]; assert len(c)==1,(g,pre,[x.name for x in c]); return c[0]
CS='by-use-case/customer-service/goals/conversation-resolution'; SS='by-use-case/support-services/goals'; OPS='cross-cutting/operations/goals'
LIB={ # key: (goal path, file prefix)
 'f_falsecomp':(CS,'false-completion-claim'),'f_politeclose':(SS+'/issue-resolution','premature-ticket-closure'),'f_repeatcontact':(SS+'/issue-resolution','repeat-contact-loop'),'f_deflect':(SS+'/self-service-deflection','deflection-of-unresolved'),
 'f_productline':(SS+'/ticket-routing','agent-infers-product-line'),'f_kbstale':(SS+'/issue-resolution','knowledgebase-staleness'),'f_lowconf':(SS+'/self-service-deflection','low-retrieval-confidence'),'f_halluconf':('cross-cutting/accuracy/goals/output-accuracy','hallucination-confidence-miscalibration'),
 'f_poorescal':(CS,'poor-escalation'),'f_escearly':(CS,'escalation-too-early'),'f_chatloop':(SS+'/self-service-deflection','chatbot-loop'),'f_sentdelay':(SS+'/sentiment-escalation','sentiment-misclassification'),
 'f_repeatq':(CS,'repeated-question-loop'),'f_unclearnext':(CS,'unclear-next-step'),'f_overapology':(CS,'over-apology-loop'),'f_circfaq':(SS+'/self-service-deflection','circular-faq-redirect-loop'),'f_tone':(CS,'tone-mismatch'),
 'f_unverifiedrefund':(SS+'/issue-resolution','unverified-customer-claim'),'f_handoffapproval':(OPS+'/agent-handoffs-delegation','handoff-approval-skipped'),
 'f_irrev':('by-capability/external-actions/goals/action-execution','irreversible-action-without-confirmation'),
 'f_piiexp':('cross-cutting/security/goals/data-loss-prevention','pii-exposure'),'f_memprivacy':(OPS+'/memory-management','memory-privacy-boundary-violation'),'f_memleak':(OPS+'/memory-safety','memory-privilege-leak'),
 'f_injection':('cross-cutting/security/goals/security-autonomy','indirect-prompt-injection'),
 'f_inconsistent':(CS,'inconsistent-answers'),'f_silentmodel':('by-capability/reasoning-and-thought/goals/model-updates-and-versioning','silent-model-update'),
 'f_badrefusal':(CS,'bad-refusal'),'f_refusalinc':('by-capability/reasoning-and-thought/goals/model-behavior-and-capabilities','model-refusal-inconsistency'),
 'f_unauthcommit':('by-capability/speech-and-audio/goals/conversation-flow','unauthorized-commitments'),'f_aidisc':('by-capability/speech-and-audio/goals/conversation-flow','ai-disclosure-failures'),
 'f_ownerverify':('cross-cutting/security/goals/tool-authorization-limits','owner-verification-not-enforced'),
 'f_fabcite':('by-capability/knowledge-retrieval/goals/citation-accuracy','fabricated-citations'),'f_misground':('by-capability/knowledge-retrieval/goals/citation-accuracy','misgrounded-citation'),'f_unsupported':('by-capability/knowledge-retrieval/goals/citation-accuracy','unsupported-claim'),'f_wrongsource':('by-capability/knowledge-retrieval/goals/citation-accuracy','wrong-source'),
 'f_sycophancy':('cross-cutting/accuracy/goals/reasoning-quality','sycophancy'),
}
HM={'f_flagship':'goals/conversation-leadership/failures/answer-and-go-conversation.md','f_stakes':'goals/stakes-calibration/failures/stakes-blind-register.md','f_empathy':'goals/emotional-intelligence/failures/hollow-empathy.md','f_undisclosed':'goals/trust-and-rapport/failures/undisclosed-bot-identity.md','f_deesc':'goals/difficult-customers/failures/no-de-escalation-strategy.md','f_crisis':'goals/vulnerable-users/failures/missed-crisis-signals.md','f_child':'goals/age-adaptation/failures/child-user-treated-as-adult.md','f_style':'goals/cultural-adaptation/failures/one-size-communication-style.md','f_fair':'goals/fairness-and-identity/failures/dialect-and-name-quality-gap.md','f_negotiation':'goals/relational-and-boundaries/failures/negotiation-capitulation.md','f_visual':'goals/channel-selection/failures/visual-product-sold-by-text-or-voice.md','f_complex':'goals/channel-selection/failures/complex-or-emotional-discussion-forced-into-chat.md','f_handoff':'goals/channel-selection/failures/no-channel-switch-or-context-lost.md','f_sensitive':'goals/channel-selection/failures/sensitive-data-collected-in-chat.md'}
CAND={'c_ax01':'AX-01','c_ax02':'AX-02','c_ax06':'AX-06','c_dm03':'DM-03','c_dm08':'DM-08','c_rf01':'RF-01','c_rf02':'RF-02','c_rf03':'RF-03','c_hu01':'HU-01','c_hu04':'HU-04','c_mo01':'MO-01','c_pv03':'PV-03','c_pv04':'PV-04','c_cc16':'CC-16','c_cc11':'CC-11','c_cc09':'CC-09','c_cc10':'CC-10','c_rp02':'RP-02','c_gv40':'GV-40','c_ex19':'EX-19','c_ex20':'EX-20','c_cc08':'CC-08','c_cp06':'CP-06','c_cp01':'CP-01','c_gv38':'GV-38','c_vi03':'VI-03','c_cc17':'CC-17','c_em24':'EM-24','c_cd01':'CD-01','c_cd02':'CD-02','c_cd03':'CD-03','c_cd04':'CD-04'}
cat={}
for f in glob.glob(str(HMI/'roadmap/*.md')):
    for l in open(f):
        m=re.match(r'\| ([A-Z]{2}-\d+) \| (.+?) \|',l)
        if m: cat[m.group(1)]=m.group(2)
F={}
for k,(g,pre) in LIB.items():
    f=find(g,pre); F[k]=dict(title=h1(f),issue=issue(f),path=str(f.relative_to(R)),kind='library')
for k,p in HM.items():
    f=HMI/p; assert f.exists(),p; F[k]=dict(title=h1(f).split(': ')[-1] if ': ' in h1(f) else h1(f),issue=issue(f) if '## Issue' in f.read_text() else '',path=str(f.relative_to(R)),kind='written')
    # HMI pages have no Issue heading; use a short summary line instead
for k,i in CAND.items(): F[k]=dict(title=cat[i],issue='Catalogued candidate, not yet written. ID '+i,path=None,kind='candidate')
# short summaries for written HMI patterns
SUM={'f_flagship':'The bot answers, then stops: no next step, no closure.','f_stakes':'Same breezy tone and improvised facts for a funeral as for store hours.','f_empathy':'"I understand your frustration," on repeat, with no action.','f_undisclosed':'Hides that it is an AI, or what it cannot do.','f_deesc':'Quotes policy at angry customers and never changes tactics.','f_crisis':'Carries on with the task while a user signals crisis.','f_child':'Collects data and pushes sales on a likely child.','f_style':'Same directness, idioms, and formality for everyone.','f_fair':'Unequal service by dialect, name, or identity cues.','f_negotiation':'Gives away discounts, or gets tricked into a bad deal.','f_visual':'Selling fashion or furniture with words only.','f_complex':'A hard conversation stuck in a chat window.','f_handoff':'Customers repeat themselves after a handoff.','f_sensitive':'Card numbers and SSNs typed into a chat or spoken to a bot.'}
for k,s in SUM.items(): F[k]['issue']=s
json.dump(F,open(HERE/'failures.json','w'),indent=1)
print(len(F),'failures')
