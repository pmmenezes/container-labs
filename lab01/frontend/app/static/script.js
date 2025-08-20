document.getElementById('fetchDataButton').addEventListener('click', async () => {
    const dataOutput = document.getElementById('dataOutput');
    dataOutput.innerHTML = 'Obtendo dados...';

    try {
        const response = await fetch('/api/data');
        const data = await response.json();

        if (response.ok) {
            dataOutput.innerHTML = `Dados obtidos com sucesso: <pre>${JSON.stringify(data, null, 2)}</pre>`;
        } else {
            dataOutput.innerHTML = `Erro ao obter dados: <pre>${JSON.stringify(data, null, 2)}</pre>`;
        }
    } catch (error) {
        dataOutput.innerHTML = `Ocorreu um erro: ${error.message}`;
    }
});