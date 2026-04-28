import os

filepath = "assets/index-CX0ZRKD4.js"
with open(filepath, "rb") as f:
    content = f.read()

# Marcadores para encontrar a função ZR
url_marker = rb"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"
start_marker = rb"const ZR=async r=>{let t=localStorage.getItem"

idx_url = content.find(url_marker)
idx_start = content.rfind(start_marker, 0, idx_url)
# O fim da função costuma ser antes deorts ou im=
idx_end = content.find(rb"catch(o){console.error", idx_url)
if idx_end != -1:
    idx_end = content.find(rb"}}", idx_end) + 2

if idx_start != -1 and idx_end != -1:
    print(f"Updating ZR from {idx_start} to {idx_end}")

    # Nova função v1
    minified_zr = (
        rb'const ZR=async r=>{let t=localStorage.getItem("GEMINI_API_KEY");'
        rb'if(!t||t==="null"||t==="undefined"){t=prompt("Por favor, insira sua GEMINI_API_KEY para gerar o patch:\\n(Ela ser\xe1 salva apenas no seu navegador)");'
        rb'if(t)localStorage.setItem("GEMINI_API_KEY",t)}if(!t)throw new Error("GEMINI_API_KEY \xe9 necess\xe1ria para gerar o patch.");'
        rb'const n="Voc\xea \xe9 um expert no sintetizador Casio CZ-101 (Phase Distortion). Sua tarefa \xe9 gerar patches que correspondam \xe0 descri\xe7\xe3o do usu\xe1rio. Responda APENAS com um objeto JSON puro, sem markdown, seguindo exatamente esta estrutura: {toneName: string, lineSelect: \\\"1\\\"|\\\"2\\\"|\\\"1+1\\\"|\\\"1+2\\\", modulation: {ring: boolean, noise: boolean}, detune: {sign: \\\"+\\\"|\\\"-\\\", octave: 0-3, note: 0-11, fine: 0-60}, vibrato: {wave: 1-4, delay: 0-99, rate: 0-99, depth: 0-99}, octave: {sign: \\\"+\\\"|\\\"-\\\", range: 0-1}, line1: {dco: {waveFirst: 1-8, waveSecond: 0-8, env: {steps: [{rate: 0-99, level: 0-99, susEnd: \\\"NONE\\\"|\\\"SUS\\\"|\\\"END\\\"}]}}, dcw: {keyFollow: 0-9, env: {steps: [...]}}, dca: {keyFollow: 0-9, env: {steps: [...]}}}, line2: (mesma estrutura que line1 ou null se lineSelect for \\\"1\\\") , comment: string}. Envelopes devem ter de 1 a 8 steps.";'
        rb'const s=await fetch(`https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key=${t}`,{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({contents:[{role:"user",parts:[{text:n+"\\n\\nDescri\xe7\xe3o do som: "+r}]}]})});'
        rb'if(!s.ok){const o=await s.json();if(s.status===400||s.status===401){localStorage.removeItem("GEMINI_API_KEY");throw new Error("Chave API inv\xe1lida ou sem acesso ao modelo Flash. Verifique sua chave.")}throw new Error("Erro na API Gemini: "+(o.error?o.error.message:s.statusText))}'
        rb'const u=await s.json();try{let text=u.candidates[0].content.parts[0].text;text=text.replace(/```json/g,"").replace(/```/g,"").trim();return JSON.parse(text)}catch(o){console.error("Erro ao parsear resposta da IA:",o,u);throw new Error("A IA gerou um formato inv\xe1lido. Tente novamente.")}}'
    )

    new_content = content[:idx_start] + minified_zr + content[idx_end:]
    with open(filepath, "wb") as f:
        f.write(new_content)
    print("Success: Updated to v1 API")
else:
    print(f"Failed to find bounds. start={idx_start}, url={idx_url}, end={idx_end}")
