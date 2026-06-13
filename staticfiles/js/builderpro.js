/* ============================================================
   Builder Pro — Main JavaScript
   ============================================================ */

// ── Theme: the app is always dark (no light mode toggle needed,
//    but we keep the icon flip for the "sun" UX signal)
document.addEventListener('DOMContentLoaded', function () {
    updateThemeIcon();
    initTooltips();
    autoHideAlerts();
    initChartDefaults();
    highlightActiveSidebarLink();
});

/* ── Dark Mode Toggle ──────────────────────────────────────── */
function toggleDarkMode() {
    // The base theme is already dark; this toggles a "light-override" class
    document.body.classList.toggle('light-override');
    const isLight = document.body.classList.contains('light-override');
    localStorage.setItem('lightMode', isLight);
    updateThemeIcon();
}

function updateThemeIcon() {
    const icon = document.getElementById('themeIcon');
    if (!icon) return;
    const isLight = localStorage.getItem('lightMode') === 'true';
    icon.className = isLight ? 'fas fa-moon' : 'fas fa-sun';
    if (isLight) document.body.classList.add('light-override');
}

/* ── Sidebar Toggle (mobile) ───────────────────────────────── */
function toggleSidebar() {
    const sidebar  = document.getElementById('sidebar');
    const content  = document.getElementById('content');
    if (!sidebar) return;
    sidebar.classList.toggle('active');
    if (content) content.classList.toggle('sidebar-open');
}

// Close sidebar when clicking outside (mobile)
document.addEventListener('click', function (e) {
    const sidebar = document.getElementById('sidebar');
    const toggle  = document.getElementById('sidebarToggle');
    if (!sidebar) return;
    if (window.innerWidth <= 768 &&
        sidebar.classList.contains('active') &&
        !sidebar.contains(e.target) &&
        toggle && !toggle.contains(e.target)) {
        sidebar.classList.remove('active');
    }
});

/* ── Highlight active sidebar link ─────────────────────────── */
function highlightActiveSidebarLink() {
    const currentPath = window.location.pathname;
    document.querySelectorAll('.sidebar .nav-link').forEach(link => {
        if (link.getAttribute('href') === currentPath) {
            link.classList.add('active');
        }
    });
}

/* ── Tooltips ──────────────────────────────────────────────── */
function initTooltips() {
    const triggers = document.querySelectorAll('[data-bs-toggle="tooltip"]');
    triggers.forEach(el => new bootstrap.Tooltip(el));
}

/* ── Auto-hide alerts ──────────────────────────────────────── */
function autoHideAlerts() {
    setTimeout(function () {
        document.querySelectorAll('.alert-dismissible').forEach(function (alert) {
            try { new bootstrap.Alert(alert).close(); } catch (_) {}
        });
    }, 6000);
}

/* ── Chart.js global defaults ──────────────────────────────── */
function initChartDefaults() {
    if (typeof Chart === 'undefined') return;
    Chart.defaults.font.family  = "'Inter', 'Segoe UI', system-ui, sans-serif";
    Chart.defaults.font.size    = 12;
    Chart.defaults.color        = '#94a3b8';
    Chart.defaults.borderColor  = 'rgba(99,102,241,0.12)';
    Chart.defaults.plugins.legend.labels.color = '#94a3b8';
    Chart.defaults.plugins.legend.labels.padding = 16;
    Chart.defaults.scale = Chart.defaults.scale || {};
    Chart.defaults.scale.grid = { color: 'rgba(99,102,241,0.08)' };
}

/* ── WBS Tree Toggle ───────────────────────────────────────── */
function toggleWBS(icon) {
    const parent   = icon.closest('li');
    const children = parent.querySelector('ul');
    if (!children) return;
    const isHidden = children.style.display === 'none' || children.style.display === '';
    children.style.display = isHidden ? 'block' : 'none';
    icon.textContent = isHidden ? '−' : '+';
}

/* ── Confirm Delete ────────────────────────────────────────── */
function confirmDelete(event, message) {
    if (!confirm(message || 'Are you sure you want to delete this item?')) {
        event.preventDefault();
    }
}

/* ── PERT Probability Calculator ───────────────────────────── */
function calculateProbability() {
    const targetDays       = parseFloat(document.getElementById('targetDays')?.value);
    const expectedDuration = parseFloat(document.getElementById('expectedDuration')?.value);
    const stdDev           = parseFloat(document.getElementById('stdDev')?.value);

    if (isNaN(targetDays) || isNaN(expectedDuration) || isNaN(stdDev) || stdDev === 0) return;

    const z           = (targetDays - expectedDuration) / stdDev;
    const probability = 0.5 * (1 + erf(z / Math.sqrt(2))) * 100;

    const resultEl = document.getElementById('probabilityResult');
    const zEl      = document.getElementById('zScoreResult');
    if (resultEl) resultEl.textContent = probability.toFixed(2) + '%';
    if (zEl)      zEl.textContent      = z.toFixed(4);

    const bar = document.getElementById('probabilityBar');
    if (bar) {
        bar.style.width = Math.min(probability, 100) + '%';
        bar.setAttribute('aria-valuenow', Math.min(probability, 100));
        bar.className = 'progress-bar ' +
            (probability >= 70 ? 'bg-success' : probability >= 40 ? 'bg-warning' : 'bg-danger');
    }
}

function erf(x) {
    const a1 = 0.254829592, a2 = -0.284496736, a3 = 1.421413741;
    const a4 = -1.453152027, a5 = 1.061405429, p = 0.3275911;
    const sign = x < 0 ? -1 : 1;
    x = Math.abs(x);
    const t = 1 / (1 + p * x);
    const y = 1 - (((((a5 * t + a4) * t) + a3) * t + a2) * t + a1) * t * Math.exp(-x * x);
    return sign * y;
}

/* ── AJAX PERT Probability ─────────────────────────────────── */
function fetchPertProbability(projectId, targetDays) {
    fetch(`/activities/pert/${projectId}/probability/?target_days=${targetDays}`, {
        headers: { 'X-Requested-With': 'XMLHttpRequest' }
    })
    .then(r => r.json())
    .then(data => {
        const el = document.getElementById('probResult');
        if (!el) return;
        el.innerHTML = `
            <div class="alert alert-info">
                <strong>Probability of Completion:</strong> ${data.probability}%<br>
                <strong>Expected Duration:</strong> ${data.expected_duration} days<br>
                <strong>Standard Deviation:</strong> ${data.standard_deviation} days<br>
                <strong>Z-Score:</strong> ${((data.target_days - data.expected_duration) / data.standard_deviation).toFixed(4)}
            </div>`;
    })
    .catch(err => console.error('PERT fetch error:', err));
}
