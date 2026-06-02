const watchlist = [
  {ticker:"SQM-B", name:"Soc. Química y Minera de Chile", price:"$ 54.620", ret:4.21, rsi:"63,4", vol:"24,1%", signal:"ALZA", color:"blue", trend:[12,16,14,20,18,22,16,19,21,20,25,24,29,28,34]},
  {ticker:"COPEC", name:"Empresas Copec S.A.", price:"$ 7.450", ret:1.28, rsi:"55,2", vol:"18,7%", signal:"VIGILAR", color:"yellow", trend:[18,19,23,21,25,19,22,20,24,21,23,22,25,24,27]},
  {ticker:"FALABELLA", name:"Falabella S.A.", price:"$ 2.610", ret:-0.76, rsi:"45,1", vol:"22,3%", signal:"VIGILAR", color:"yellow", trend:[16,17,17,19,18,22,16,21,20,19,18,20,19,20,18]},
  {ticker:"CENCOSUD", name:"Cencosud S.A.", price:"$ 1.360", ret:0.37, rsi:"52,8", vol:"19,2%", signal:"VIGILAR", color:"yellow", trend:[13,16,20,18,22,19,17,20,19,21,20,22,21,23,22]},
  {ticker:"CHILE", name:"Banco de Chile", price:"$ 116,20", ret:2.91, rsi:"61,7", vol:"17,6%", signal:"ALZA", color:"green", trend:[14,16,15,18,17,19,16,20,22,21,24,26,25,29,31]},
  {ticker:"PROVIDA", name:"Provida AFP", price:"$ 1.248", ret:-1.12, rsi:"38,6", vol:"21,8%", signal:"RIESGO", color:"red", trend:[25,23,19,20,16,18,15,19,18,17,19,18,20,17,18]},
];

const market = [
  {idx:"IPSA", last:"6.538,32", varp:0.67, trend:[9,11,10,13,12,16,14,18,17,20]},
  {idx:"IGPA", last:"33.012,45", varp:0.58, trend:[11,12,13,12,15,14,16,18,17,20]},
  {idx:"SPCLXIPSA", last:"4.275,11", varp:0.71, trend:[8,11,10,12,13,14,13,15,17,19]},
  {idx:"DOW JONES", last:"39.872,99", varp:-0.12, trend:[19,18,17,18,16,17,15,16,15,17]},
  {idx:"S&P 500", last:"5.321,41", varp:0.09, trend:[10,11,10,12,11,13,14,13,15,16]},
  {idx:"NASDAQ", last:"16.832,62", varp:0.32, trend:[8,10,9,11,12,14,13,15,17,18]},
];

function formatDateCL(){
  const now = new Date();
  return now.toLocaleString("es-CL", {
    day:"2-digit", month:"long", year:"numeric",
    hour:"2-digit", minute:"2-digit"
  }) + " CLT";
}

function sparkline(values, colorClass="green", width=116, height=30){
  const min = Math.min(...values), max = Math.max(...values);
  const denom = Math.max(max - min, 1);
  const points = values.map((v,i)=>{
    const x = (i/(values.length-1))*width;
    const y = height - ((v-min)/denom)*(height-6) - 3;
    return `${x.toFixed(1)},${y.toFixed(1)}`;
  }).join(" ");
  const colors = {green:"#2bd981", red:"#ff4759", yellow:"#ffd34f", blue:"#4d8dff"};
  return `<svg class="spark" viewBox="0 0 ${width} ${height}" preserveAspectRatio="none">
    <polyline points="${points}" fill="none" stroke="${colors[colorClass]||colors.green}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
  </svg>`;
}

function drawWatchlist(data = watchlist){
  const tbody = document.getElementById("watchlistBody");
  tbody.innerHTML = data.map(row => {
    const signalClass = row.signal.toLowerCase();
    const retClass = row.ret >= 0 ? "positive" : "negative";
    const retText = `${row.ret >= 0 ? "+" : ""}${row.ret.toFixed(2).replace(".",",")}%`;
    const sparkColor = row.signal === "ALZA" ? "green" : row.signal === "RIESGO" ? "red" : "yellow";
    return `<tr>
      <td>
        <div class="asset-cell">
          <span class="star">☆</span>
          <span class="asset-dot dot-${row.color}"></span>
          <div class="asset-meta"><strong>${row.ticker}</strong><small>${row.name}</small></div>
        </div>
      </td>
      <td>${row.price}</td>
      <td class="${retClass}">${retText}</td>
      <td>${row.rsi}</td>
      <td>${row.vol}</td>
      <td><span class="signal ${signalClass}">${row.signal}</span></td>
      <td>${sparkline(row.trend, sparkColor)}</td>
      <td class="more">···</td>
    </tr>`;
  }).join("");
}

function drawMarket(){
  const tbody = document.getElementById("marketBody");
  tbody.innerHTML = market.map(row => {
    const pos = row.varp >= 0;
    const c = pos ? "green" : "red";
    const varText = `${pos ? "+" : ""}${row.varp.toFixed(2).replace(".",",")}%`;
    return `<tr>
      <td>${row.idx}</td><td>${row.last}</td>
      <td class="${pos ? "positive" : "negative"}">${varText}</td>
      <td>${sparkline(row.trend, c, 70, 20).replace('class="spark"', 'class="mini-spark"')}</td>
    </tr>`;
  }).join("");
}

function drawMainChart(){
  const canvas = document.getElementById("mainChart");
  const ctx = canvas.getContext("2d");
  const dpr = window.devicePixelRatio || 1;
  const rect = canvas.getBoundingClientRect();
  canvas.width = rect.width * dpr;
  canvas.height = rect.height * dpr;
  ctx.scale(dpr, dpr);

  const w = rect.width, h = rect.height;
  ctx.clearRect(0,0,w,h);

  const pad = {l:22, r:64, t:12, b:42};
  const plotW = w - pad.l - pad.r;
  const plotH = h - pad.t - pad.b;

  // grid
  ctx.strokeStyle = "rgba(210,230,255,.12)";
  ctx.lineWidth = 1;
  ctx.font = "12px Inter";
  ctx.fillStyle = "rgba(220,232,248,.86)";
  const yLabels = ["6.600","6.400","6.200","6.000","5.800","5.600"];
  for(let i=0;i<6;i++){
    const y = pad.t + i*(plotH/5);
    ctx.beginPath(); ctx.moveTo(pad.l,y); ctx.lineTo(pad.l+plotW,y); ctx.stroke();
    ctx.fillText(yLabels[i], pad.l+plotW+16, y+4);
  }
  const xLabels = ["22 Abr","29 Abr","6 May","13 May","20 May"];
  for(let i=0;i<xLabels.length;i++){
    const x = pad.l + i*(plotW/(xLabels.length-1));
    ctx.fillText(xLabels[i], x-22, h-13);
  }

  const n = 42;
  const prices = [];
  let price = 5940;
  for(let i=0;i<n;i++){
    const drift = i > 25 ? 23 : i > 13 ? -4 : 12;
    const noise = Math.sin(i*1.7)*48 + Math.cos(i*.57)*29;
    price += drift + noise*0.08;
    prices.push(price + Math.sin(i*.42)*130);
  }
  // Force rising end
  for(let i=30;i<n;i++) prices[i] += (i-30)*24;

  const minP = 5600, maxP = 6660;
  const mapX = i => pad.l + i*(plotW/(n-1));
  const mapY = p => pad.t + (maxP-p)/(maxP-minP)*plotH;

  // volume bars
  for(let i=0;i<n;i++){
    const x = mapX(i);
    const barH = 8 + Math.abs(Math.sin(i*1.9))*24;
    ctx.fillStyle = "rgba(47,96,161,.15)";
    ctx.fillRect(x-4, pad.t+plotH-barH, 8, barH);
  }

  // Moving average lines
  function drawLine(vals, color, width=1.5){
    ctx.strokeStyle=color; ctx.lineWidth=width; ctx.beginPath();
    vals.forEach((v,i)=>{ const x=mapX(i), y=mapY(v); i?ctx.lineTo(x,y):ctx.moveTo(x,y); });
    ctx.stroke();
  }
  const ma20 = prices.map((p,i)=> prices.slice(Math.max(0,i-4),i+1).reduce((a,b)=>a+b,0)/Math.min(i+1,5));
  const ma50 = prices.map((p,i)=> 5900 + i*5.5 + Math.sin(i*.23)*34);
  const ma200 = prices.map((p,i)=> 5760 + i*2.6 + Math.cos(i*.16)*20);

  // Candles
  for(let i=0;i<n;i++){
    const x = mapX(i);
    const open = prices[i] + Math.sin(i*2.1)*48;
    const close = prices[i] + Math.cos(i*1.35)*48 + (i>30?35:0);
    const high = Math.max(open,close)+34+Math.abs(Math.sin(i))*22;
    const low = Math.min(open,close)-30-Math.abs(Math.cos(i))*18;
    const up = close >= open;
    ctx.strokeStyle = up ? "#2bd981" : "#ff4759";
    ctx.fillStyle = up ? "#2bd981" : "#ff4759";
    ctx.lineWidth = 1.3;
    ctx.beginPath(); ctx.moveTo(x, mapY(low)); ctx.lineTo(x, mapY(high)); ctx.stroke();
    const y = Math.min(mapY(open), mapY(close));
    const bodyH = Math.max(Math.abs(mapY(open)-mapY(close)), 5);
    ctx.fillRect(x-4.2, y, 8.4, bodyH);
  }

  drawLine(ma20, "#4d8dff", 1.6);
  drawLine(ma50, "#d82835", 1.4);
  drawLine(ma200, "rgba(190,204,224,.55)", 1.4);

  // Price tag
  const lastY = mapY(6538.32);
  ctx.fillStyle = "#2bd981";
  roundRect(ctx, pad.l+plotW-4, lastY-13, 62, 26, 4);
  ctx.fill();
  ctx.fillStyle = "#fff";
  ctx.font = "700 12px Inter";
  ctx.fillText("6.538,32", pad.l+plotW+2, lastY+4);
}

function roundRect(ctx,x,y,w,h,r){
  ctx.beginPath();
  ctx.moveTo(x+r,y);
  ctx.arcTo(x+w,y,x+w,y+h,r);
  ctx.arcTo(x+w,y+h,x,y+h,r);
  ctx.arcTo(x,y+h,x,y,r);
  ctx.arcTo(x,y,x+w,y,r);
  ctx.closePath();
}

function refreshNumbers(){
  document.getElementById("timestamp").textContent = formatDateCL();
  const base = 6538.32 + (Math.random()*20-10);
  document.getElementById("ipsaValue").textContent = base.toLocaleString("es-CL",{minimumFractionDigits:2,maximumFractionDigits:2});
  const ch = 0.45 + Math.random()*0.4;
  document.getElementById("ipsaChange").textContent = `+${ch.toFixed(2).replace(".",",")}% (${(base*ch/100).toFixed(2).replace(".",",")})`;
}

function init(){
  drawWatchlist();
  drawMarket();
  refreshNumbers();
  setTimeout(drawMainChart, 60);
  window.addEventListener("resize", drawMainChart);
  document.getElementById("refreshButton").addEventListener("click", () => {
    refreshNumbers();
    drawMainChart();
    document.getElementById("refreshButton").textContent = "Actualizado";
    setTimeout(()=>document.getElementById("refreshButton").textContent="Actualizar", 1300);
  });
  document.getElementById("sortButton").addEventListener("click", () => {
    const order = {ALZA:0,VIGILAR:1,RIESGO:2};
    drawWatchlist([...watchlist].sort((a,b)=>order[a.signal]-order[b.signal]));
  });
  document.getElementById("searchInput").addEventListener("input", (e) => {
    const q = e.target.value.trim().toLowerCase();
    drawWatchlist(watchlist.filter(x => x.ticker.toLowerCase().includes(q) || x.name.toLowerCase().includes(q)));
  });
}

init();
