import re

filepath = "assets/index-CX0ZRKD4.js"
with open(filepath, "rb") as f:
    content = f.read()

# Marcador da função ZR que inseri anteriormente (agora com localStorage)
# Vou buscar pelo início e fim conhecidos
start_marker = rb"const ZR=async r=>{let t=localStorage.getItem"
end_marker = rb'throw new Error("A IA gerou um formato inv\xe1lido. Tente novamente.")}}'

start_idx = content.find(start_marker)
end_idx = content.find(end_marker)

if start_idx != -1 and end_idx != -1:
    end_idx += len(end_marker)

    # Nova função usando a versão v1 da API
    minified_zr = (
        rb'const ZR=async r=>{let t=localStorage.getItem("GEMINI_API_KEY");'
        rb'if(!t||t==="null"||t==="undefined"){t=prompt("Por favor, insira sua GEMINI_API_KEY para gerar o patch:\\n(Ela ser\xe1 salva apenas no seu navegador)");'
        rb'if(t)localStorage.setItem("GEMINI_API_KEY",t)}if(!t)throw new Error("GEMINI_API_KEY \xe9 necess\xe1ria para gerar o patch.");'
        rb'const n="Voc\xea \xe9 um expert no sintetizador Casio CZ-101 (Phase Distortion). Sua tarefa \xe9 gerar patches que correspondam \xe0 descri\xe7\xe3o do usu\xe1rio. Responda APENAS com um objeto JSON puro, sem markdown, seguindo exatamente esta estrutura: {toneName: string, lineSelect: \\\"1\\\"|\\\"2\\\"|\\\"1+1\\\"|\\\"1+2\\\", modulation: {ring: boolean, noise: boolean}, detune: {sign: \\\"+\\\"|\\\"-\\\", octave: 0-3, note: 0-11, fine: 0-60}, vibrato: {wave: 1-4, delay: 0-99, rate: 0-99, depth: 0-99}, octave: {sign: \\\"+\\\"|\\\"-\\\", range: 0-1}, line1: {dco: {waveFirst: 1-8, waveSecond: 0-8, env: {steps: [{rate: 0-99, level: 0-99, susEnd: \\\"NONE\\\"|\\\"SUS\\\"|\\\"END\\\"}]}}, dcw: {keyFollow: 0-9, env: {steps: [...]}}, dca: {keyFollow: 0-9, env: {steps: [...]}}}, line2: (mesma estrutura que line1 ou null se lineSelect for \\\"1\\\") , comment: string}. Envelopes devem ter de 1 a 8 steps.";'
        # Alterado de v1beta para v1 abaixo:
        rb'const s=await fetch(`https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key=${t}`,{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({contents:[{role:"user",parts:[{text:n+"\\n\\nDescri\xe7\xe3o do som: "+r}]}]})});'
        rb'if(!s.ok){const o=await s.json();if(s.status===400||s.status===401){localStorage.removeItem("GEMINI_API_KEY");throw new Error("Chave API inv\xe1lida ou sem acesso ao modelo Flash. Verifique sua chave.")}throw new Error("Erro na API Gemini: "+(o.error?o.error.message:s.statusText))}'
        rb'const u=await s.json();try{let text=u.candidates[0].content.parts[0].text;text=text.replace(/```json/g,"").replace(/```/g,"").trim();return JSON.parse(text)}catch(o){console.error("Erro ao parsear resposta da IA:",o,u);throw new Error("A IA gerou um formato inv\xe1lido. Tente novamente.")}}'
    )

    new_content = content[:start_idx] + minified_zr + content[end_idx:]
    with open(filepath, "wb") as f:
        f.write(new_content)
    print("Patch v2 (API v1) applied successfully.")
else:
    print(f"Could not find ZR function to update. start={start_idx}, end={end_idx}")
