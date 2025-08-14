window.PG = (function(){
	const initTooltips = () => {
		try{
			if (window.bootstrap && bootstrap.Tooltip){
				const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
				tooltipTriggerList.forEach(el => new bootstrap.Tooltip(el))
			}
		}catch(e){/* no-op */}
	};
	const toast = (msg, variant='primary') => {
		const c = document.getElementById('pgToasts');
		if (!c) return;
		const el = document.createElement('div');
		el.className = `toast align-items-center text-bg-${variant} border-0`;
		el.role = 'status'; el.ariaLive='polite'; el.ariaAtomic='true';
		el.innerHTML = `<div class="d-flex"><div class="toast-body">${msg}</div><button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button></div>`;
		c.appendChild(el);
		if (window.bootstrap && bootstrap.Toast) new bootstrap.Toast(el,{delay:3000}).show();
	};
	const searchGlobal = (form) => {
		const q = new FormData(form).get('q')||'';
		if (!q.trim()) return false;
		window.location.href = `/admin/workorders/workorder/?q=${encodeURIComponent(q)}`;
		return false;
	};
	const showAbout = () => toast('Taller PG — Versión local', 'secondary');

	// Admin: change list enhancements (floating + Agregar)
	const enhanceChangeList = () => {
		const cl = document.getElementById('changelist');
		if (!cl) return;
		const add = document.querySelector('.object-tools .addlink, .addlink');
		const path = location.pathname;
		let label = 'Crear nuevo';
		if (path.includes('/admin/workorders/workorder/')) label = 'Crear nueva orden de trabajo';
		else if (path.includes('/admin/customers/cliente/')) label = 'Crear nuevo cliente';
		else if (path.includes('/admin/customers/vehiculo/')) label = 'Crear nuevo vehículo';
		if (add){
			const fab = document.createElement('a');
			fab.href = add.getAttribute('href');
			fab.className = 'pg-fab';
			fab.title = label;
			fab.setAttribute('aria-label', label);
			fab.textContent = '+';
			document.body.appendChild(fab);
		}
		// Toggle filters
		const btnFilters = document.getElementById('pg-toggle-filters');
		const searchPanel = document.getElementById('changelist-search');
		if (btnFilters && searchPanel){
			btnFilters.addEventListener('click', (e)=>{ e.preventDefault(); searchPanel.hidden = !searchPanel.hidden; });
		}
	};

	// Admin: change form enhancements (fieldsets to tabs)
	const enhanceChangeForm = () => {
		const form = document.querySelector('body.change-form #content form');
		if (!form) return;
		const sets = form.querySelectorAll('fieldset');
		if (sets.length < 2) return; // tabs only if multiple sections
		// build tabs
		const nav = document.createElement('div');
		nav.className = 'pg-tabs';
		const ul = document.createElement('ul');
		ul.className = 'pg-tabs-nav';
		nav.appendChild(ul);
		sets.forEach((fs, idx) => {
			const legend = fs.querySelector('h2, legend');
			const name = legend ? legend.textContent.trim() : `Sección ${idx+1}`;
			const id = `pg-tab-${idx}`;
			fs.setAttribute('data-pg-tab', id);
			const li = document.createElement('li');
			li.innerHTML = `<button type="button" class="pg-tab-btn" data-target="${id}">${name}</button>`;
			ul.appendChild(li);
			if (idx !== 0) fs.style.display = 'none';
		});
		form.prepend(nav);
		ul.addEventListener('click', (e) => {
			const btn = e.target.closest('.pg-tab-btn');
			if (!btn) return;
			const target = btn.getAttribute('data-target');
			sets.forEach(fs => { fs.style.display = (fs.getAttribute('data-pg-tab') === target) ? '' : 'none'; });
			ul.querySelectorAll('.pg-tab-btn').forEach(b => b.classList.toggle('active', b === btn));
		});
		const firstBtn = ul.querySelector('.pg-tab-btn');
		if (firstBtn) firstBtn.classList.add('active');
	};

	const init = () => {
		initTooltips();
		enhanceChangeList();
		enhanceChangeForm();
	};

	document.addEventListener('DOMContentLoaded', init);
	return {toast, searchGlobal, showAbout};
})();