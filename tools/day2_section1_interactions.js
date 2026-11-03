/* Inlined by build_day2_section1.py; deterministic teaching examples only. */
function bindDayTwoOpening() {
    const relu = document.querySelector('[data-relu]');
    const input = relu.querySelector('input');
    function updateRelu() {
        const count = Number(input.value);
        const z = 1.6 - 0.2 * count, h = Math.max(0, z);
        const x = 440 + (z + 3) / 6 * 900, y = 420 - h / 3 * 365;
        const point = relu.querySelector('[data-relu-point]');
        point.querySelector('path').setAttribute('d', `M${x} 420 L${x} ${y}`);
        point.querySelector('circle').setAttribute('cx', x);
        point.querySelector('circle').setAttribute('cy', y);
        relu.querySelector('[data-relu-readout]').textContent = `CGCG = ${count} → z = ${z.toFixed(1)} → h = ${h.toFixed(1)}`;
        input.setAttribute('aria-valuetext', `${count} CGCG occurrences; score ${z.toFixed(1)}; activation ${h.toFixed(1)}`);
    }
    input.addEventListener('input', updateRelu);
    relu.querySelectorAll('[data-count]').forEach(button => button.addEventListener('click', () => {
        input.value = button.dataset.count;
        updateRelu();
    }));
    updateRelu();

    const hidden = document.querySelector('[data-hidden-layer]');
    hidden.querySelectorAll('[data-unit]').forEach(button => button.addEventListener('click', () => {
        const index = Number(button.dataset.unit);
        hidden.querySelectorAll('[data-unit-path]').forEach(path => path.style.opacity = Number(path.dataset.unitPath) === index ? 1 : .16);
        hidden.querySelectorAll('[data-unit]').forEach(item => item.setAttribute('aria-pressed', String(item === button)));
        hidden.querySelector('[data-unit-weights]').textContent = ['0.6, 0.8, −0.2','−0.3, 0.2, 0.5','0.2, −0.5, 0.1'][index];
        hidden.querySelector('[data-unit-bias]').textContent = ['bias −0.4','bias −0.1','bias −0.4'][index];
        hidden.querySelector('[data-unit-activation]').textContent = ['h₁ = ReLU(1.0) = 1.0','h₂ = ReLU(1.0) = 1.0','h₃ = ReLU(−0.2) = 0.0'][index];
        hidden.querySelector('[data-unit-readout]').textContent = `h${['₁','₂','₃'][index]}: own weights + own bias → ReLU → ${[1,1,0][index].toFixed(1)}`;
    }));

    const forward = document.querySelector('[data-forward]');
    const next = forward.querySelector('[data-forward-next]');
    let stage = 0;
    const descriptions = [
        'Start with one sequence’s counts.',
        'Hidden features: h₁ = 1, h₂ = 1, h₃ = 0.',
        'Output score: 1.2 × 1 − 0.7 × 1 + 0.5 × 0 − 0.2 = 0.3.',
        'Sigmoid(0.3) ≈ 0.574 → P(B).',
    ];
    function updateForward() {
        forward.querySelectorAll('[data-unit-path]').forEach(path => path.style.opacity = stage >= 1 ? 1 : .12);
        forward.querySelector('[data-forward-part="output"]').style.opacity = stage >= 2 ? 1 : .12;
        forward.querySelector('[data-forward-part="probability"]').style.opacity = stage >= 3 ? 1 : .12;
        forward.querySelector('[data-forward-readout]').textContent = descriptions[stage];
        next.textContent = ['Trace the prediction', 'Combine the features', 'Apply sigmoid', 'Prediction complete'][stage];
        next.disabled = stage === 3;
    }
    next.addEventListener('click', () => { stage = Math.min(3, stage + 1); updateForward(); });
    forward.querySelector('[data-forward-reset]').addEventListener('click', () => { stage = 0; updateForward(); });
    updateForward();
    // Print every stage at full contrast, restoring the teaching state afterwards.
    addEventListener('beforeprint', () => forward.querySelectorAll('[data-unit-path], [data-forward-part]').forEach(part => {
        part.dataset.screenOpacity = part.style.opacity;
        part.style.opacity = 1;
    }));
    addEventListener('afterprint', () => forward.querySelectorAll('[data-unit-path], [data-forward-part]').forEach(part => {
        part.style.opacity = part.dataset.screenOpacity;
    }));
}
