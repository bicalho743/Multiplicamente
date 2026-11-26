import sys
R="/home/user/Multiplicamente"
FONT=f"file://{R}/www/fonts/nunito-latin.woff2"
def phone(img, w=640, h=980, ox=200, oy=530, cw=690, ch=1390, extra=""):
    # recorta só o celular da imagem de loja (1080x1920) e ajusta ao tamanho w x h
    sc = w/cw
    return f'''<div class="phone" style="width:{w}px;height:{h}px;{extra}"><img src="file://{R}/marketing/loja/{img}" style="width:{1080*sc}px;left:{-ox*sc}px;top:{-oy*sc}px"></div>'''
chip='<div class="chip">🦉 MultiplicaMente</div>'
def slide(n, cls, inner):
    return f'<section class="slide {cls}">{chip}{inner}<div class="pg">{n}/7</div></section>'
slides=[
 slide(1,"s1",f'''<h1>Tabuada<br>sem choro?</h1><p class="sub">Seu filho aprende brincando.</p>
   <div class="deslize">deslize →</div>{phone("01_jornada.png", extra="position:absolute;left:220px;top:790px;")}'''),
 slide(2,"s2",'''<h2>Decorar sem entender cansa</h2>
   <div class="bigcard"><div class="q">7 × 8 = ?</div><div class="face">😩</div></div>
   <p class="body dark">Repetir a conta até a cabeça doer não ensina o <b>porquê</b> do resultado.</p>'''),
 slide(3,"s3",f'''<h2>Aqui a conta<br>vira desenho</h2>
   <p class="body">Com a ajuda, os grupos mostram o que é multiplicar. Errou? O app explica a resposta certa.</p>
   {phone("02_conta.png", w=560, h=700, extra="position:absolute;left:260px;top:690px;")}'''),
 slide(4,"s4",f'''<h2>Cada vitória resgata uma criatura</h2>
   <p class="body">São <b>180 criaturas</b> para colecionar, em 4 operações.</p>
   {phone("03_vitoria.png", w=400, h=806, extra="position:absolute;left:340px;top:530px;")}'''),
 slide(5,"s5",f'''<h2>Você acompanha tudo</h2>
   <p class="body">Relatório para os pais: precisão, dias seguidos e progresso por tabuada, protegido por PIN.</p>
   {phone("08_relatorio.png", w=560, h=640, extra="position:absolute;left:260px;top:720px;")}'''),
 slide(6,"s6",'''<h2>Sem anúncios.<br>Sem internet.</h2>
   <ul class="list"><li>✅ Funciona offline</li><li>✅ Nenhum anúncio</li><li>✅ Nuvem só se você quiser</li></ul>
   <div class="price"><div><b>Grátis</b><span>tabuadas do 2 ao 6</span></div><div><b>R$ 9,99</b><span>versão completa · pagamento único</span></div></div>'''),
 slide(7,"s7",'''<div class="owl">🦉</div><h2>Procure <u>MultiplicaMente</u><br>na Google Play</h2>
   <p class="body">Para crianças de 6 a 10 anos.</p>
   <div class="save">💾 Salve este post para a hora da lição de casa</div>'''),
]
css=f'''
@font-face{{font-family:Nunito;src:url({FONT}) format("woff2");font-weight:200 1000;}}
*{{box-sizing:border-box;margin:0;padding:0}} body{{background:#222;font-family:Nunito,sans-serif}}
.slide{{position:relative;width:1080px;height:1350px;overflow:hidden;color:#fff;padding:120px 80px 0}}
.chip{{position:absolute;top:48px;left:80px;background:rgba(255,255,255,.22);color:#fff;border-radius:100px;padding:12px 26px;font-weight:800;font-size:30px}}
.pg{{position:absolute;bottom:40px;right:60px;font-weight:800;font-size:28px;opacity:.75}}
h1{{font-size:150px;line-height:1;font-weight:900;margin-top:70px;letter-spacing:-3px}}
h2{{font-size:96px;line-height:1.05;font-weight:900;margin-top:60px;letter-spacing:-2px}}
.sub{{font-size:58px;font-weight:800;margin-top:34px}}
.body{{font-size:48px;line-height:1.3;font-weight:700;margin-top:34px;max-width:900px}}
.dark{{color:#3c3c3c}} .deslize{{position:absolute;left:80px;top:640px;font-size:38px;font-weight:800;background:#fff;color:#2e8b00;border-radius:100px;padding:14px 30px}}
.phone{{overflow:hidden;border-radius:64px;box-shadow:0 30px 70px rgba(0,0,0,.35)}} .phone img{{position:absolute;display:block}}
.s1{{background:linear-gradient(160deg,#58cc02,#2f9e00)}} .s2{{background:#fff4d6;color:#3c3c3c}} .s2 .chip{{background:rgba(0,0,0,.08);color:#3c3c3c}} .s2 .pg{{color:#3c3c3c}}
.s3{{background:linear-gradient(160deg,#1cb0f6,#7a5cff)}} .s4{{background:linear-gradient(160deg,#ff9600,#ff4b4b)}}
.s5{{background:linear-gradient(160deg,#9b5cff,#5b2bd6)}} .s6{{background:linear-gradient(160deg,#58cc02,#1cb0f6)}}
.s7{{background:linear-gradient(160deg,#58cc02,#2f9e00);text-align:center}} .s7 .body{{margin-left:auto;margin-right:auto}}
.bigcard{{margin:60px auto 0;background:#fff;border-radius:56px;padding:60px;text-align:center;box-shadow:0 20px 50px rgba(0,0,0,.15)}}
.q{{font-size:190px;font-weight:900;color:#3c3c3c}} .face{{font-size:150px;margin-top:10px}}
.list{{list-style:none;margin-top:50px}} .list li{{font-size:56px;font-weight:800;margin-top:22px}}
.price{{display:flex;gap:28px;margin-top:60px}} .price div{{flex:1;background:#fff;color:#3c3c3c;border-radius:40px;padding:36px 30px;text-align:center}}
.price b{{display:block;font-size:84px;font-weight:900;color:#2e8b00}} .price span{{display:block;font-size:34px;font-weight:700;margin-top:8px}}
.owl{{font-size:260px;margin-top:40px}} .s7 h2{{margin-top:20px}} u{{text-decoration-thickness:8px;text-underline-offset:10px}}
.save{{margin:60px auto 0;display:inline-block;background:#fff;color:#2e8b00;border-radius:100px;padding:28px 50px;font-weight:900;font-size:44px}}
'''
open(sys.argv[1],'w',encoding='utf-8').write(f'<!doctype html><meta charset="utf-8"><style>{css}</style>'+''.join(slides))
