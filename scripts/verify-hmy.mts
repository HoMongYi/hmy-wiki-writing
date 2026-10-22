/** Read-only native integration. No HMY schema/parser copies. */
import fs from "node:fs/promises"
import { accessSync as requireAsset } from "node:fs"
import path from "node:path"
import { createRequire } from "node:module"
import { pathToFileURL, fileURLToPath } from "node:url"
import assert from "node:assert/strict"
import { createHash } from "node:crypto"
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),"..")
const flag=process.argv.indexOf("--hmy-root")
if(flag<0 || !process.argv[flag+1]) throw new Error("Provide --hmy-root <actual project>")
const hmy=path.resolve(process.argv[flag+1])
const req=createRequire(path.join(hmy,"site/package.json"))
const native=async (rel:string)=>import(pathToFileURL(path.join(hmy,rel)).href)
const dep=async (name:string)=>import(pathToFileURL(req.resolve(name)).href)
const core=await native("packages/hmy-wiki-core/src/index.ts")
const {isSafelyEditable}=await native("obsidian-plugin/src/editing.ts")
const {validateAdvancedBlock}=await native("obsidian-plugin/src/blockValidation.ts")
const {scanVault,resolveWikiLink}=await native("site/scripts/lib/hardware-audit.mjs")
const {parseDocument}=await dep("yaml")
const {unified}=await dep("unified")
const {default:remarkParse}=await dep("remark-parse")
const {default:GithubSlugger}=await dep("github-slugger")
const vault=path.join(root,"examples/fixtures/vault")
const index=await scanVault(vault)
const errors:string[]=[]
const kinds=new Set<string>()
const specimens:any[]=[]
const featureChecks:string[]=[]
let negativeChecks=6
let blocks=0,links=0,images=0,roundtrips=0,outputCases=0,outputBlocks=0
const unverifiedAssets:Array<{case:string,src:string,reason:string}>=[]
const md=(s:string)=>unified().use(remarkParse).parse(s)
const walk=(n:any,fn:(n:any)=>void)=>{fn(n);for(const c of n.children??[])walk(c,fn)}
const content=new Map<string,string>()
for(const d of index.documents)content.set(d.path,await fs.readFile(path.join(vault,d.path),"utf8"))
const headingIds=new Map<string,Set<string>>()
for(const [rel,text] of content){
 const slugger=new GithubSlugger(),ids=new Set<string>()
 walk(md(text),(n:any)=>{if(n.type==="heading"){let label="";walk(n,(c:any)=>{if(c.type==="text"||c.type==="inlineCode")label+=c.value});ids.add(slugger.slug(label))}})
 headingIds.set(rel,ids)
}
function inspectBlocks(text:string,label:string,assetRoot?:string){
 walk(md(text),(n:any)=>{
  if(n.type!=="code"||!n.lang?.startsWith("hmy-"))return
  blocks++;kinds.add(n.lang)
  const model=core.parseHmyBlock(n.lang,n.value)
  if(!model){errors.push(label+": parser rejected "+n.lang);return}
  specimens.push(model)
  const html=core.renderHmyBlock(model)
  if(!html)errors.push(label+": empty render")
  if(/<script[ >]/i.test(html))errors.push(label+": executable output")
  if(model.kind==="hmy-media")for(const media of [model.media,model.media.compare].filter(Boolean)){
   if(!assetRoot || /^https?:/i.test(media.src)){
    unverifiedAssets.push({case:label,src:media.src,reason:assetRoot?"Remote image existence is not checked":"Provide --outputs-assets-root to verify model image files"});continue
   }
   const dest=path.resolve(assetRoot,media.src.replace(/^\/+/,""))
   if(!dest.startsWith(assetRoot+path.sep)){errors.push(label+": escaping block image");continue}
   try{requireAsset(dest)}catch{errors.push(label+": missing block image "+media.src)}
  }
  if(!isSafelyEditable(n.lang,n.value))errors.push(label+": GUI cannot preserve fields")
  const invalid=validateAdvancedBlock(model)
  if(invalid)errors.push(label+": "+invalid)
  const restored=core.parseHmyBlock(n.lang,core.serializeStructuredBlock(model))
  try{assert.deepEqual(restored,model);roundtrips++}catch{errors.push(label+": roundtrip changed model")}
 })
}
for(const [rel,text] of content){
 const fm=text.match(/^---\r?\n([\s\S]*?)\r?\n---/)?.[1]
 const doc=parseDocument(fm??"",{uniqueKeys:true,strict:true})
 if(doc.errors.length)errors.push(rel+": invalid Frontmatter")
 if(!core.isPublicDocument(doc.toJS()??{}))errors.push(rel+": fixture excluded by status")
 inspectBlocks(text,rel,vault)
 for(const m of text.matchAll(/(?<!!)\[\[([^\]]+)\]\]/g)){
  links++;const target=resolveWikiLink(m[1],index)
  if(!target){errors.push(rel+": unresolved "+m[1]);continue}
  const heading=m[1].split("|")[0].split("#")[1]
  if(heading&&!headingIds.get(target.path)?.has(new GithubSlugger().slug(heading)))errors.push(rel+": missing heading "+m[1])
 }
 for(const m of text.matchAll(/!\[[^\]]*\]\(([^)]+)\)/g)){
  if(/^[a-z]+:/i.test(m[1]))continue
  images++;const dest=path.resolve(path.dirname(path.join(vault,rel)),decodeURIComponent(m[1]))
  if(!dest.startsWith(vault+path.sep))errors.push(rel+": escaping image")
  try{await fs.access(dest)}catch{errors.push(rel+": missing image")}
 }
}
inspectBlocks(await fs.readFile(path.join(root,"examples/hmy-blocks.md"),"utf8"),"block specimens",vault)
const fixtureBlocks=blocks
const outputFlag=process.argv.indexOf("--outputs")
if(outputFlag>=0){
 assert.ok(process.argv[outputFlag+1],"--outputs needs a JSON path")
 const output=JSON.parse(await fs.readFile(path.resolve(process.argv[outputFlag+1]),"utf8"))
 assert.ok(output && typeof output==="object" && Array.isArray(output.cases) && output.cases.length>0,"--outputs requires a nonempty cases array")
 const assetFlag=process.argv.indexOf("--outputs-assets-root")
 const assetRoot=assetFlag>=0?path.resolve(process.argv[assetFlag+1]??""):undefined
 if(assetFlag>=0){assert.ok(process.argv[assetFlag+1],"--outputs-assets-root needs a directory");assert.ok((await fs.stat(assetRoot!)).isDirectory(),"Model asset root must exist")}
 const ids=new Set<string>()
 for(const c of output.cases){
  assert.ok(c && typeof c==="object" && !Array.isArray(c),"Every output case must be an object")
  const id=c.id??c.mode
  assert.ok(typeof id==="string" && id.trim() && !ids.has(id),"Output cases need unique nonempty IDs (legacy mode names also accepted)")
  assert.equal(typeof c.markdown,"string",id+": markdown must be explicitly provided")
  assert.ok(c.markdown.trim() || (typeof c.report==="string" && c.report.trim()),id+": empty Markdown needs a Review Only report")
  ids.add(id);outputCases++
  const before=blocks;inspectBlocks(c.markdown,id,assetRoot);outputBlocks+=blocks-before
 }
}
assert.equal(resolveWikiLink("메모리 트레이닝",index)?.path,"01_하드웨어/Memory Training.md")
assert.equal(resolveWikiLink("RAM Timing",index)?.path,"01_하드웨어/메모리 타이밍.md")
const missing=core.parseHmyBlock("hmy-diagnosis","steps:\n  - id: start\n    title: 확인\n    yes: missing")
assert.ok(missing,"Native parser boundary changed; review")
assert.ok(validateAdvancedBlock(missing),"GUI must reject missing branch ID")
assert.equal(core.parseHmyBlock("hmy-diagnosis","steps: ["),null)
assert.equal(isSafelyEditable("hmy-spec","type: custom\ngroups:\n  - items:\n      - label: A\n        value: B\n        invented: C"),false)
assert.equal(core.isPublicDocument({visibility:"private"}),false)
assert.equal(core.isPublicDocument({visibility:"public",status:"draft"}),false)
assert.equal(core.isPublicDocument({visibility:"public",status:"verified",legal_risk:"high"}),false)
for(const k of core.HMY_BLOCK_LANGUAGES)if(!kinds.has(k))errors.push("Untested native language: "+k)
function rejected(kind:string,body:string){
 negativeChecks++
 assert.equal(core.parseHmyBlock(kind,body),null,`Must reject invalid ${kind}`)
}
const body=(m:any)=>core.serializeStructuredBlock(m)
const signal=specimens.find(m=>m.kind==="hmy-signal")
const plot=specimens.find(m=>m.kind==="hmy-spec"&&m.plot)
const diagram=specimens.find(m=>m.kind==="hmy-diagram")
const explorers=specimens.filter(m=>m.kind==="hmy-explorer")
assert.ok(signal&&plot&&diagram&&explorers.length>=2,"Missing visual coverage")
const s=signal.signal
rejected("hmy-signal",body({...signal,signal:{...s,mode:"measured"}}))
rejected("hmy-signal",body({...signal,signal:{...s,channels:[{...s.channels[0],states:["high"]}]}}))
rejected("hmy-signal",body({...signal,signal:{...s,source:"javascript:alert(1)"}}))
rejected("hmy-spec",body({...plot,plot:{...plot.plot,max:0}}))
rejected("hmy-spec",body({...plot,plot:{...plot.plot,source:"not-a-url"}}))
const groups=JSON.parse(JSON.stringify(plot.groups));groups[0].items[0].value="7.88 GB/s"
rejected("hmy-spec",body({...plot,groups}))
const d=diagram.diagram
rejected("hmy-diagram",body({...diagram,diagram:{...d,edges:[{...d.edges[0],to:"missing"}]}}))
rejected("hmy-diagram",body({...diagram,diagram:{...d,nodes:[d.nodes[0],d.nodes[0]]}}))
rejected("hmy-diagram",body(diagram)+"\nscript: alert(1)")
const directed="steps:\n  - id: start\n    text: 확인\n    choices:\n      - {label: 결과, target: missing}"
rejected("hmy-diagnosis",directed)
rejected("hmy-diagnosis",directed.replace("target: missing","target: start"))
for(const m of explorers){
 const b=m.explorer
 assert.match(core.renderHmyBlock(m),/<table/)
 assert.match(core.renderHmyBlock(m),/hmy-explorer-baseline/)
 if(b.kind==="ddr-cas"){
  rejected("hmy-explorer",body({...m,explorer:{...b,baseline:{dataRate:0,cl:30}}}))
  rejected("hmy-explorer",body({...m,explorer:{...b,baseline:{dataRate:6000,cl:1.5}}}))
  rejected("hmy-explorer",body({...m,explorer:{...b,baseline:{dataRate:6000,cl:129}}}))
 }else{
  rejected("hmy-explorer",body({...m,explorer:{...b,baseline:{generation:6,lanes:4}}}))
  rejected("hmy-explorer",body({...m,explorer:{...b,baseline:{generation:4,lanes:3}}}))
 }
 rejected("hmy-explorer",body(m)+"\nformula: made-up")
}
assert.equal(core.casLatency(6000,30),10)
assert.ok(Math.abs(core.casLatency(5600,40)!-14.2857142857)<1e-8)
const expected=[1,2,3.9384615384615387,7.876923076923077,15.753846153846155]
expected.forEach((value,i)=>{
 assert.ok(Math.abs(core.pcieBandwidth(i+1,4)!-value)<1e-10)
 assert.equal(plot.groups[0].items[i].value,value.toFixed(2),"Plot and independent calculation differ")
})
featureChecks.push("10-language specimen coverage","visual static fallback","diagnosis targets/cycles","diagram endpoints/IDs/unknown fields","signal conceptual-only","plot units/context/source/range","DDR CAS and PCIe1-5 independent values","Obsidian save and roundtrip","local media comparison assets")
const provenance:any={}
for(const dir of ["packages/hmy-wiki-core/src","packages/hmy-wiki-core/styles"]){
 for(const name of await fs.readdir(path.join(hmy,dir))){
  const rel=dir+"/"+name,stat=await fs.stat(path.join(hmy,rel));if(!stat.isFile())continue
  provenance[rel]=createHash("sha256").update(await fs.readFile(path.join(hmy,rel))).digest("hex")
 }
}
for(const rel of ["obsidian-plugin/src/editing.ts","obsidian-plugin/src/blockValidation.ts","obsidian-plugin/src/visualBlocks.ts","obsidian-plugin/src/main.ts","site/quartz/hmy/blocks.ts","site/quartz/hmy/visuals.inline.ts"]){
 provenance[rel]=createHash("sha256").update(await fs.readFile(path.join(hmy,rel))).digest("hex")
}
console.log(JSON.stringify({status:errors.length?"Failed":unverifiedAssets.length?"Needs verification":"Passed",documents:index.documents.length,blocks,fixture_blocks:fixtureBlocks,output_cases:outputCases,output_blocks:outputBlocks,unverified_assets:unverifiedAssets,kinds:[...kinds].sort(),links,images,roundtrips,negative_checks:negativeChecks,feature_checks:featureChecks,provenance,errors,scope:"Native YAML/remark/core/Obsidian editability+validation+serialization and Vault resolver; app UI/full Quartz build separate."},null,2))
process.exitCode=errors.length?1:unverifiedAssets.length?2:0
