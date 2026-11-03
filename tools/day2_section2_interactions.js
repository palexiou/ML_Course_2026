/* Deterministic teaching constructions. No model fitting or external requests. */
function bindDayTwoLearning() {
    const panels = Object.fromEntries([...document.querySelectorAll('[data-learning]')].map(p => [p.dataset.learning, p]));
    const q = (panel, selector) => panel.querySelector(selector);
    const read = (panel, value) => { const node = q(panel, '[data-learning-readout]'); if (node) node.textContent = value; };
    const sigmoid = z => 1 / (1 + Math.exp(-z));
    const ns = 'http://www.w3.org/2000/svg';
    function shape(parent, tag, attrs) {
        const node = document.createElementNS(ns, tag);
        for (const [key, value] of Object.entries(attrs)) node.setAttribute(key, value);
        parent.append(node);
        return node;
    }
    function overlay(panel, key) {
        const chart = q(panel, `[data-chart="${key}"]`), d = Object.fromEntries(Object.entries(chart.dataset).map(([k,v]) => [k, Number(v)]));
        const group = q(chart, '[data-chart-overlay]');
        group.replaceChildren();
        return { group, x: v => d.x + (v - d.xmin) / (d.xmax - d.xmin) * d.w, y: v => d.y + d.h - (v - d.ymin) / (d.ymax - d.ymin) * d.h, bottom: d.y + d.h };
    }
    function dot(plot, x, y, color = '#0072B2', radius = 13) {
        shape(plot.group, 'circle', {cx: plot.x(x), cy: plot.y(y), r: radius, fill: color, stroke: 'white', 'stroke-width': 3});
    }
    function path(plot, points, color, width = 5, dash = '') {
        shape(plot.group, 'polyline', {points: points.map(([x,y]) => `${plot.x(x)},${plot.y(y)}`).join(' '), fill: 'none', stroke: color, 'stroke-width': width, 'stroke-dasharray': dash});
    }

    const parameter = panels.parameters;
    q(parameter, '[data-parameter="bias"]').style.opacity = .12;
    parameter.querySelectorAll('[data-parameter-select]').forEach(button => button.addEventListener('click', () => {
        parameter.querySelectorAll('[data-parameter]').forEach(group => group.style.opacity = group.dataset.parameter === button.dataset.parameterSelect ? 1 : .12);
        parameter.querySelectorAll('[data-parameter-select]').forEach(item => item.setAttribute('aria-pressed', String(item === button)));
    }));
    q(panels.forward, '[data-label-reveal]').addEventListener('click', event => {
        q(panels.forward, '[data-observed-label]').style.opacity = 1;
        event.currentTarget.disabled = true;
    });

    const loss = panels.loss;
    function lossPoint(probability) {
        const value = -Math.log(probability), plot = overlay(loss, 'loss');
        shape(plot.group, 'path', {d: `M${plot.x(probability)} ${plot.bottom} L${plot.x(probability)} ${plot.y(value)}`, fill: 'none', stroke: '#0072B2', 'stroke-width': 3, 'stroke-dasharray': '8 8'});
        dot(plot, probability, value);
        read(loss, `P(B) ≈ ${probability.toFixed(3)} → loss ≈ ${value.toFixed(3)} · observed B / y = 1`);
    }
    loss.querySelectorAll('[data-probability]').forEach(button => button.addEventListener('click', () => lossPoint(button.dataset.probability === 'current' ? sigmoid(.3) : Number(button.dataset.probability))));
    lossPoint(sigmoid(.3));

    const gradient = panels.gradient, weight = q(gradient, 'input');
    function weightPoint() {
        const v = Number(weight.value), value = Math.log1p(Math.exp(.9 - v)), g = sigmoid(v - .9) - 1, plot = overlay(gradient, 'weight');
        const left = Math.max(.8,v-.07), right = Math.min(1.6,v+.07);
        path(plot, [[left, value+(left-v)*g], [right, value+(right-v)*g]], '#0072B2', 5);
        dot(plot, v, value);
        weight.setAttribute('aria-valuetext', `Output weight ${v.toFixed(2)}, loss ${value.toFixed(3)}, gradient ${g.toFixed(3)}`);
        read(gradient, `v₁ = ${v.toFixed(2)} → loss ≈ ${value.toFixed(3)} · local gradient ≈ ${g.toFixed(3)}`);
    }
    weight.addEventListener('input', weightPoint);
    gradient.querySelectorAll('[data-weight]').forEach(button => button.addEventListener('click', () => { weight.value = button.dataset.weight; weightPoint(); }));
    weightPoint();

    const backprop = panels.backprop;
    let backwardStage = 0;
    function backward() {
        ['output','hidden','earlier'].forEach((key, index) => q(backprop, `[data-backward="${key}"]`).style.opacity = backwardStage > index ? 1 : .08);
        const next = q(backprop, '[data-backward-next]');
        next.disabled = backwardStage === 3;
        next.textContent = ['Trace loss sensitivity','Reach the hidden layer','Reach earlier parameters','Gradients computed'][backwardStage];
    }
    q(backprop, '[data-backward-next]').addEventListener('click', () => { backwardStage = Math.min(3, backwardStage + 1); backward(); });
    q(backprop, '[data-backward-reset]').addEventListener('click', () => { backwardStage = 0; backward(); });
    backward();

    const update = panels.update, initial = 1.2, g = sigmoid(.3) - 1, moved = initial - .1*g;
    let stepped = false;
    function updatePoint() {
        const plot = overlay(update, 'update'), value = v => Math.log1p(Math.exp(.9-v));
        dot(plot, initial, value(initial), '#0072B2', 12);
        if (stepped) {
            path(plot, [[initial,value(initial)],[moved,value(moved)]], '#D55E00', 5, '9 7');
            dot(plot, moved, value(moved), '#D55E00', 15);
        }
        const v = stepped ? moved : initial;
        q(update, '[data-weight-step]').disabled = stepped;
        read(update, `v₁ = ${v.toFixed(3)} → P(B) ≈ ${sigmoid(v-.9).toFixed(3)} → loss ≈ ${value(v).toFixed(3)}`);
    }
    q(update, '[data-weight-step]').addEventListener('click', () => { stepped = true; updatePoint(); });
    q(update, '[data-weight-reset]').addEventListener('click', () => { stepped = false; updatePoint(); });
    updatePoint();

    const rate = panels.rate;
    let rateStep = 0;
    function ratePaths() {
        for (const [key, eta, color] of [['small',.2,'#0072B2'],['large',1.1,'#D55E00']]) {
            const plot = overlay(rate, key), points = [];
            let w = 3;
            for (let i=0; i<=rateStep; i++) { points.push([w,(w-1)**2]); w -= eta*2*(w-1); }
            path(plot, points, color, 4, '8 5');
            points.forEach(([x,y]) => dot(plot, x, y, color, 8));
            dot(plot, ...points[points.length-1], color, 12);
        }
        q(rate, '[data-rate-next]').disabled = rateStep === 6;
        read(rate, `Same starting weight, different step sizes · step ${rateStep} of 6`);
    }
    q(rate, '[data-rate-next]').addEventListener('click', () => { rateStep = Math.min(6, rateStep + 1); ratePaths(); });
    q(rate, '[data-rate-reset]').addEventListener('click', () => { rateStep = 0; ratePaths(); });
    ratePaths();

    const epoch = panels.epoch;
    let pass = 1, batch = 0;
    function epochView() {
        epoch.querySelectorAll('[data-epoch-batch]').forEach(group => {
            const index = Number(group.dataset.epochBatch);
            group.classList.toggle('done', index < batch);
            group.classList.toggle('current', index === batch && batch < 12);
            const first = index*64;
            q(group, '[data-epoch-rows]').textContent = pass === 1 ? `Rows ${first+1}–${Math.min(720,first+64)}` : `${(first*31+(pass-1)*137)%720+1}, ${((first+1)*31+(pass-1)*137)%720+1}, …`;
        });
        q(epoch, '[data-epoch-next]').textContent = batch === 12 ? 'Begin next epoch' : 'Next update';
        const examples = Math.min(720, batch*64);
        read(epoch, `Epoch ${pass} · ${batch} / 12 updates · ${examples} / 720 examples${pass > 1 ? ' · reshuffled row order' : ''}`);
    }
    q(epoch, '[data-epoch-next]').addEventListener('click', () => { if (batch === 12) { pass++; batch = 0; } else batch++; epochView(); });
    q(epoch, '[data-epoch-reset]').addEventListener('click', () => { pass = 1; batch = 0; epochView(); });
    epochView();

    const code = panels.code;
    let codeLine = 0;
    const operations = ['Clear old gradients before the next minibatch.','Forward: compute logits using the current weights.','Loss: compare logits with this minibatch’s labels.','Backward: compute gradients, keeping weights unchanged.','Step: Adam uses the gradients to update parameters.'];
    function codeView() {
        code.querySelectorAll('[data-code-line]').forEach(line => line.classList.toggle('current', Number(line.dataset.codeLine) === codeLine));
        q(code, '[data-code-next]').disabled = codeLine === 4;
        read(code, operations[codeLine]);
    }
    q(code, '[data-code-next]').addEventListener('click', () => { codeLine = Math.min(4,codeLine+1); codeView(); });
    q(code, '[data-code-reset]').addEventListener('click', () => { codeLine = 0; codeView(); });
    codeView();

    const validation = panels.validation, epochs = [1,8,16,24], scores = [.62,.66,.64,.63];
    let selected = false;
    function checkpoint() {
        const best = scores.reduce((best, score, index) => score > scores[best] ? index : best, 0);
        for (const [key, values, color] of [['train',[.66,.61,.54,.48],'#0072B2'],['validation',scores,'#D55E00']]) {
            const plot = overlay(validation,key);
            epochs.forEach((x,index) => dot(plot,x,values[index],color,9));
            if (selected) {
                shape(plot.group, 'path', {d: `M${plot.x(epochs[best])} ${plot.bottom} L${plot.x(epochs[best])} ${plot.y(values[best])}`, fill:'none',stroke:'#D55E00','stroke-width':4,'stroke-dasharray':'10 8'});
                dot(plot,epochs[best],values[best],'#D55E00',16);
            }
        }
        if (selected) read(validation,`Selected epoch ${epochs[best]} · highest validation ROC-AUC ${scores[best].toFixed(2)} · training still runs to epoch 24`);
        q(validation,'[data-select-checkpoint]').disabled = selected;
    }
    q(validation,'[data-select-checkpoint]').addEventListener('click', () => { selected = true; checkpoint(); });
    checkpoint();

    let saved;
    addEventListener('beforeprint', () => {
        saved = {backwardStage,stepped,rateStep,pass,batch,selected,opacity:[]};
        document.querySelectorAll('.day-two-learning [data-parameter], .day-two-learning [data-observed-label]').forEach(part => { saved.opacity.push([part,part.style.opacity]); part.style.opacity = 1; });
        backwardStage=3; stepped=true; rateStep=6; batch=12; selected=true;
        backward(); updatePoint(); ratePaths(); epochView(); checkpoint();
    });
    addEventListener('afterprint', () => {
        if (!saved) return;
        ({backwardStage,stepped,rateStep,pass,batch,selected} = saved);
        saved.opacity.forEach(([part,opacity]) => part.style.opacity = opacity);
        backward(); updatePoint(); ratePaths(); epochView(); checkpoint();
        if (!selected) read(validation,'Training improves; validation does not keep improving.');
    });
}
