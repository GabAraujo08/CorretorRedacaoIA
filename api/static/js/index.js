// Selecione o botão e o textarea
const btnCopiar = document.getElementById('btnColar');
const meuTextarea = document.getElementById('redacao');

// Adicione um ouvinte de evento de clique ao botão
btnCopiar.addEventListener('click', function () {
    // Verifique se há algo na área de transferência do usuário
    if (navigator.clipboard) {
        // Cole o conteúdo da área de transferência no textarea
        navigator.clipboard.readText().then(function (clipboardText) {
            meuTextarea.value = clipboardText;
        }).catch(function (err) {
            console.error('Erro ao acessar a área de transferência:', err);
        });
    } else {
        // Se a API de área de transferência não estiver disponível, você pode pedir ao usuário para colar manualmente.
        meuTextarea.placeholder = 'Cole (Ctrl+V) o texto aqui';
    }
});
