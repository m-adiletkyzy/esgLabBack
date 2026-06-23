document.addEventListener('DOMContentLoaded', function () {
    const wordFileInputRu = document.querySelector('input[name="word_fileRu"]');
    const wordFileInputEn = document.querySelector('input[name="word_fileEn"]');
    const wordFileInputKk = document.querySelector('input[name="word_fileKk"]');

    const rutextField = document.querySelector('textarea[name="Rutext"]');
    const engtextField = document.querySelector('textarea[name="Engtext"]');
    const kktextField = document.querySelector('textarea[name="Kktext"]');

    function handleFileUpload(inputFile, textField) {
        if (inputFile && textField) {
            inputFile.addEventListener('change', function (e) {
                const file = e.target.files[0];
                if (file && file.name.endsWith('.docx')) {
                    const reader = new FileReader();
                    reader.onload = function(event) {
                        const arrayBuffer = event.target.result;

                        // Используем библиотеку Mammoth для конвертации docx в текст
                        mammoth.extractRawText({ arrayBuffer: arrayBuffer })
                            .then(function(result) {
                                textField.value = result.value;
                            })
                            .catch(function(err) {
                                console.error(err);
                            });
                    };
                    reader.readAsArrayBuffer(file);
                }
            });
        }
    }

    // Привязываем обработчики для всех файлов
    handleFileUpload(wordFileInputRu, rutextField);
    handleFileUpload(wordFileInputEn, engtextField);
    handleFileUpload(wordFileInputKk, kktextField);
});
