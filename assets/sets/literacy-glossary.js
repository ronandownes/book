/* Book literacy and glossary enhancement. Works without changing the mathematical text.
   Authored alternatives are added only where a paragraph has been explicitly reviewed. */
(function(){
'use strict';
if(document.querySelector('[data-book-literacy]'))return;
var meanings={
'glossary-area':['Area','The surface inside a shape, measured in square units such as cm².'],
'glossary-cardinality':['Cardinality','How many different elements belong to the set. For A, write #A.'],
'glossary-complement':['Complement','Elements of the universal set that are not in the named set.'],
'glossary-element':['Element','One item that belongs to a set.'],
'glossary-height':['Height','For this rectangle, the vertical side length.'],
'glossary-intersection':['Intersection','Elements shared by both sets. Written A ∩ B.'],
'glossary-multiple':['Multiple','A whole-number multiple of 2 has the form 2n. Zero counts because 2 × 0 = 0.'],
'glossary-perimeter':['Perimeter','Distance around a shape, measured in length units such as cm.'],
'glossary-set':['Set','A well-defined collection of distinct objects. Order and repetition do not change it.'],
'glossary-union':['Union','Elements in A or in B or in both. Written A ∪ B.'],
'glossary-universal':['Universal set','All the elements being considered, often named U.'],
'glossary-width':['Width','For this rectangle, the horizontal side length.']
};
var glossary;
function ensureGlossary(){
 if(glossary)return glossary;
 glossary=document.createElement('dialog');
 glossary.setAttribute('aria-labelledby','maths-word-heading');
 glossary.className='maths-book-dialog';
 glossary.innerHTML='<h2 id="maths-word-heading">Mathematical words</h2><div class="maths-word-body" id="maths-word-body"></div><button type="button" id="maths-word-close">Close</button>';
 document.body.appendChild(glossary);
 glossary.querySelector('#maths-word-close').addEventListener('click',function(){glossary.close()});
 return glossary;
}
function openWord(slug){
 var d=ensureGlossary(), entry=meanings[slug];
 var box=d.querySelector('#maths-word-body');
 box.replaceChildren();
 if(entry){
  var dt=document.createElement('h3'),dd=document.createElement('p');
  dt.textContent=entry[0];dd.textContent=entry[1];box.append(dt,dd);
 }else{
  Object.keys(meanings).forEach(function(key){
   var heading=document.createElement('h3'),p=document.createElement('p');
   heading.textContent=meanings[key][0];p.textContent=meanings[key][1];
   box.append(heading,p);
  });
 }
 if(typeof d.showModal==='function')d.showModal();else d.setAttribute('open','');
}
document.addEventListener('click',function(event){
 var link=event.target.closest&&event.target.closest('a[href]');
 if(!link)return;
 var href=link.getAttribute('href')||'';
 var match=href.match(/(?:#|\/)(glossary-(?:set|element|cardinality|perimeter|area|multiple|intersection|union|universal|complement|width|height))(?:$|[?#])/);
 if(!match||!meanings[match[1]])return;
 event.preventDefault();event.stopImmediatePropagation();openWord(match[1]);
},true);
var variants={
'Begin with one circle. Move the elements. Then learn the notation.':{
 maths:'Begin with one circle. Move the elements. Then learn the notation.',
 eal:'Start with one circle. The items inside are elements. Move them; the set is unchanged.',
 simple:'One circle. Move the elements. Write the set.'
},
'Look. Predict. Explore. Practise. Explain. Try each question before revealing its answer.':{
 maths:'Look. Predict. Explore. Practise. Explain. Try each question before revealing its answer.',
 eal:'First look at the example. Make a guess. Try it. Explain your answer. Then check.',
 simple:'Look. Try. Check. Explain.'
}
};
var paragraphs=[];
document.querySelectorAll('p').forEach(function(p){
 var key=p.textContent.trim().replace(/\s+/g,' ');
 if(variants[key])paragraphs.push({node:p,values:variants[key]});
});
var bar=document.createElement('div');
bar.setAttribute('data-book-literacy','');
bar.setAttribute('role','group');
bar.setAttribute('aria-label','Language level');
bar.className='maths-book-literacy';
var legend=document.createElement('span');legend.textContent='Language';bar.appendChild(legend);
['maths','eal','simple'].forEach(function(mode){
 var b=document.createElement('button');b.type='button';b.dataset.language=mode;
 b.textContent=mode==='maths'?'Maths':mode==='eal'?'EAL':'Simple';
 b.addEventListener('click',function(){choose(mode)});bar.appendChild(b);
});
var words=document.createElement('button');words.type='button';words.textContent='Words';
words.addEventListener('click',function(){openWord(null)});bar.appendChild(words);
var css=document.createElement('style');
css.textContent='.maths-book-literacy{display:flex;flex-wrap:wrap;gap:5px;align-items:center;padding:8px 4px;margin:0 0 15px;color:#25425e;font:600 .8rem Arial,sans-serif}.maths-book-literacy button{border:1px solid #a6bed3;border-radius:6px;background:#fff;color:#174a76;padding:6px 10px;font:inherit;cursor:pointer}.maths-book-literacy button[aria-pressed=true]{background:#174a76;color:white}.maths-book-literacy button:last-child{margin-left:auto}.maths-book-dialog{max-width:min(92vw,510px);max-height:80vh;overflow-y:auto;padding:20px 22px;border:1px solid #abc1d5;border-radius:12px;line-height:1.5;color:#172a3b}.maths-book-dialog::backdrop{background:rgba(12,28,44,.64)}.maths-book-dialog h3{font-size:1rem;margin:12px 0 2px}.maths-book-dialog p{margin:0 0 8px}.maths-book-dialog button{background:#174a76;border:0;border-radius:6px;padding:9px 17px;color:white;cursor:pointer}';
document.head.appendChild(css);
var place=document.querySelector('main')||document.querySelector('.ptx-content')||document.querySelector('article');
if(place)place.insertBefore(bar,place.firstChild);
function choose(mode){
 if(!['maths','eal','simple'].includes(mode))mode='maths';
 paragraphs.forEach(function(item){item.node.textContent=item.values[mode]});
 bar.querySelectorAll('button[data-language]').forEach(function(b){b.setAttribute('aria-pressed',String(b.dataset.language===mode))});
 try{localStorage.setItem('maths-literacy',mode)}catch(e){}
}
var selected='maths';
try{selected=localStorage.getItem('maths-literacy')||'maths'}catch(e){}
choose(selected);
})();
