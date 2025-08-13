window.PG = (function(){
	const init = () => {
		const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
		tooltipTriggerList.forEach(el => new bootstrap.Tooltip(el))
	};
	const toast = (msg, variant='primary') => {
		const c = document.getElementById('pgToasts');
		if (!c) return;
		const el = document.createElement('div');
		el.className = `toast align-items-center text-bg-${variant} border-0`;
		el.role = 'status'; el.ariaLive='polite'; el.ariaAtomic='true';
		el.innerHTML = `<div class="d-flex"><div class="toast-body">${msg}</div><button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button></div>`;
		c.appendChild(el);
		new bootstrap.Toast(el,{delay:3000}).show();
	};
	const searchGlobal = (form) => {
		const q = new FormData(form).get('q')||'';
		if (!q.trim()) return false;
		window.location.href = `/admin/workorders/workorder/?q=${encodeURIComponent(q)}`;
		return false;
	};
	const showAbout = () => toast('Taller PG — Versión local', 'secondary');
	document.addEventListener('DOMContentLoaded', init);
	return {toast, searchGlobal, showAbout};
})();