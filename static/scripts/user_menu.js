// Alternar exibição do menu do usuário
function toggleMenu() {
    const menu = document.getElementById('dropdownMenu');
    menu.style.display = menu.style.display === 'block' ? 'none' : 'block';
}

// Fechar o menu ao clicar fora
window.addEventListener('click', function (e) {
    const menu = document.getElementById('dropdownMenu');
    const icon = document.querySelector('.user-icon');
    if (!menu.contains(e.target) && !icon.contains(e.target)) {
        menu.style.display = 'none';
    }
});

// Acionar input de imagem ao clicar na opção
function selecionarFoto() {
    document.getElementById('fotoInput').click();
}
