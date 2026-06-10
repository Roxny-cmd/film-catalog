document.addEventListener('DOMContentLoaded', function () {

    // ── Автоскрытие алертов ──
    document.querySelectorAll('.alert').forEach(function (alert) {
        setTimeout(function () {
            alert.style.transition = 'opacity 0.5s';
            alert.style.opacity = '0';
            setTimeout(function () { alert.remove(); }, 500);
        }, 4000);
    });

    // ── Дропдаун справочников ──
    var trigger = document.getElementById('dir-trigger');
    var menu    = document.getElementById('dir-menu');

    if (trigger && menu) {
        trigger.addEventListener('click', function (e) {
            e.stopPropagation();
            var isOpen = menu.classList.contains('open');
            menu.classList.toggle('open', !isOpen);
        });

        document.addEventListener('click', function () {
            menu.classList.remove('open');
        });

        menu.addEventListener('click', function (e) {
            e.stopPropagation(); // клик по пункту не закрывает до перехода
        });
    }
});

// ── Inline-редактирование справочника ──
function startEdit(id, currentName) {
    var item = document.getElementById('item-' + id);
    item.querySelector('.dir-view').classList.add('hidden');
    var form = item.querySelector('.dir-edit');
    form.classList.remove('hidden');
    form.querySelector('input[name="name"]').focus();
}
function cancelEdit(id) {
    var item = document.getElementById('item-' + id);
    item.querySelector('.dir-view').classList.remove('hidden');
    item.querySelector('.dir-edit').classList.add('hidden');
}

// ── Inline-редактирование роли актёра ──
function startCastEdit(actorId, currentRole) {
    var item = document.getElementById('cast-' + actorId);
    item.querySelector('.dir-view').classList.add('hidden');
    var form = item.querySelector('.dir-edit');
    form.classList.remove('hidden');
    form.querySelector('input[name="role"]').focus();
}
function cancelCastEdit(actorId) {
    var item = document.getElementById('cast-' + actorId);
    item.querySelector('.dir-view').classList.remove('hidden');
    item.querySelector('.dir-edit').classList.add('hidden');
}

// ── Динамические строки актёров в форме фильма ──
function addCastRow() {
    var template = document.getElementById('cast-row-template');
    if (!template) return;
    var clone = template.content.cloneNode(true);
    document.getElementById('cast-list').appendChild(clone);
}
function removeCastRow(btn) {
    btn.closest('.cast-form-row').remove();
}
