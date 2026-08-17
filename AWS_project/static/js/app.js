// ======================================================
// ELEMENTS
// ======================================================

const fileInput =
    document.getElementById("fileInput");

const dropZone =
    document.getElementById("dropZone");

const browseButton =
    document.getElementById("browseButton");

const selectedFile =
    document.getElementById("selectedFile");

const fileName =
    document.getElementById("fileName");

const fileSize =
    document.getElementById("fileSize");

const removeFile =
    document.getElementById("removeFile");

const analyzeButton =
    document.getElementById("analyzeButton");

const statsGrid =
    document.getElementById("statsGrid");

const pagesStat =
    document.getElementById("pagesStat");

const wordsStat =
    document.getElementById("wordsStat");

const sizeStat =
    document.getElementById("sizeStat");

const modelStat =
    document.getElementById("modelStat");

const modelName =
    document.getElementById("modelName");

const processingCard =
    document.getElementById("processingCard");

const processingText =
    document.getElementById("processingText");

const resultSection =
    document.getElementById("resultSection");

const summaryOutput =
    document.getElementById("summaryOutput");

const downloadButton =
    document.getElementById("downloadButton");

const toast =
    document.getElementById("toast");

const toastMessage =
    document.getElementById("toastMessage");

const statusDot =
    document.getElementById("statusDot");

const connectionStatus =
    document.getElementById("connectionStatus");


// ======================================================
// STATE
// ======================================================

let currentFile = null;


// ======================================================
// INITIALIZATION
// ======================================================

document.addEventListener(
    "DOMContentLoaded",
    () => {

        checkHealth();

        setupNavigation();

    }
);


// ======================================================
// HEALTH CHECK
// ======================================================

async function checkHealth() {

    try {

        const response =
            await fetch(
                "/api/health"
            );

        const data =
            await response.json();

        if (!data.success) {
            throw new Error(
                "Health check failed"
            );
        }

        const online =
            data.status === "online";

        if (online) {

            statusDot.classList.add(
                "online"
            );

            connectionStatus.textContent =
                data.bedrock_configured
                    ? "Connected"
                    : "AWS connected • Model not configured";

        } else {

            statusDot.classList.add(
                "error"
            );

            connectionStatus.textContent =
                "Offline";

        }


        if (
            data.model &&
            data.model !== "Not configured"
        ) {

            modelName.textContent =
                data.model;

            modelStat.textContent =
                data.model;

        }

    }

    catch (error) {

        statusDot.classList.add(
            "error"
        );

        connectionStatus.textContent =
            "Connection unavailable";

    }

}


// ======================================================
// NAVIGATION
// ======================================================

function setupNavigation() {

    const navItems =
        document.querySelectorAll(
            ".nav-item"
        );

    const views =
        document.querySelectorAll(
            ".view"
        );

    navItems.forEach(
        (item) => {

            item.addEventListener(
                "click",
                () => {

                    const target =
                        item.dataset.view;

                    navItems.forEach(
                        nav => nav.classList
                            .remove("active")
                    );

                    item.classList.add(
                        "active"
                    );


                    views.forEach(
                        view => {

                            view.classList
                                .remove(
                                    "active-view"
                                );

                        }
                    );


                    const targetView =
                        document.getElementById(
                            target
                        );

                    if (targetView) {

                        targetView.classList.add(
                            "active-view"
                        );

                    }

                }
            );

        }
    );

}


// ======================================================
// FILE BROWSER
// ======================================================

browseButton.addEventListener(
    "click",
    (event) => {

        event.stopPropagation();

        fileInput.click();

    }
);


dropZone.addEventListener(
    "click",
    () => {

        fileInput.click();

    }
);


fileInput.addEventListener(
    "change",
    (event) => {

        const file =
            event.target.files[0];

        if (file) {

            handleFile(file);

        }

    }
);


// ======================================================
// DRAG AND DROP
// ======================================================

dropZone.addEventListener(
    "dragover",
    (event) => {

        event.preventDefault();

        dropZone.classList.add(
            "dragover"
        );

    }
);


dropZone.addEventListener(
    "dragleave",
    () => {

        dropZone.classList.remove(
            "dragover"
        );

    }
);


dropZone.addEventListener(
    "drop",
    (event) => {

        event.preventDefault();

        dropZone.classList.remove(
            "dragover"
        );

        const file =
            event.dataTransfer.files[0];

        if (file) {

            handleFile(file);

        }

    }
);


// ======================================================
// FILE HANDLING
// ======================================================

function handleFile(file) {

    if (
        file.type !== "application/pdf"
        &&
        !file.name
            .toLowerCase()
            .endsWith(".pdf")
    ) {

        showToast(
            "Please select a PDF file.",
            true
        );

        return;

    }


    const maxSize =
        20 * 1024 * 1024;

    if (file.size > maxSize) {

        showToast(
            "PDF must be smaller than 20 MB.",
            true
        );

        return;

    }


    currentFile = file;


    fileName.textContent =
        file.name;

    fileSize.textContent =
        formatFileSize(
            file.size
        );


    selectedFile.classList.remove(
        "hidden"
    );

    analyzeButton.disabled =
        false;


    statsGrid.classList.add(
        "hidden"
    );

    resultSection.classList.add(
        "hidden"
    );


    showToast(
        "PDF ready for analysis."
    );

}


// ======================================================
// REMOVE FILE
// ======================================================

removeFile.addEventListener(
    "click",
    () => {

        resetFile();

    }
);


function resetFile() {

    currentFile = null;

    fileInput.value = "";

    selectedFile.classList.add(
        "hidden"
    );

    analyzeButton.disabled =
        true;

    statsGrid.classList.add(
        "hidden"
    );

    resultSection.classList.add(
        "hidden"
    );

}


// ======================================================
// ANALYZE
// ======================================================

analyzeButton.addEventListener(
    "click",
    async () => {

        if (!currentFile) {

            showToast(
                "Please choose a PDF first.",
                true
            );

            return;

        }


        const formData =
            new FormData();

        formData.append(
            "file",
            currentFile
        );


        analyzeButton.disabled =
            true;

        processingCard.classList.remove(
            "hidden"
        );

        resultSection.classList.add(
            "hidden"
        );


        processingText.textContent =
            "Uploading document to AWS S3...";


        try {

            await delay(500);


            processingText.textContent =
                "Extracting document content...";


            await delay(700);


            processingText.textContent =
                "Sending structured prompt to Amazon Bedrock...";


            const response =
                await fetch(
                    "/api/analyze",
                    {
                        method: "POST",
                        body: formData
                    }
                );


            const data =
                await response.json();


            if (!response.ok || !data.success) {

                throw new Error(
                    data.error ||
                    "Document analysis failed."
                );

            }


            processingText.textContent =
                "Generating document intelligence...";


            await delay(400);


            displayResult(
                data
            );


            showToast(
                "Document analyzed successfully."
            );

        }

        catch (error) {

            console.error(
                error
            );

            showToast(
                error.message,
                true
            );

        }

        finally {

            processingCard.classList.add(
                "hidden"
            );

            analyzeButton.disabled =
                false;

        }

    }
);


// ======================================================
// DISPLAY RESULT
// ======================================================

function displayResult(data) {

    const stats =
        data.document.statistics;


    pagesStat.textContent =
        stats.pages;

    wordsStat.textContent =
        stats.words.toLocaleString();

    sizeStat.textContent =
        `${stats.size_mb} MB`;


    modelStat.textContent =
        data.ai.model;

    modelName.textContent =
        data.ai.model;


    statsGrid.classList.remove(
        "hidden"
    );


    summaryOutput.textContent =
        data.ai.summary;


    downloadButton.href =
        data.download;


    resultSection.classList.remove(
        "hidden"
    );


    resultSection.scrollIntoView(
        {
            behavior: "smooth",
            block: "start"
        }
    );

}


// ======================================================
// TOAST
// ======================================================

function showToast(
    message,
    error = false
) {

    toastMessage.textContent =
        message;


    toast.classList.remove(
        "hidden"
    );


    if (error) {

        toast.style.borderColor =
            "rgba(255,104,104,0.3)";

    }

    else {

        toast.style.borderColor =
            "rgba(167,255,92,0.2)";

    }


    setTimeout(
        () => {

            toast.classList.add(
                "hidden"
            );

        },
        4000
    );

}


// ======================================================
// UTILITIES
// ======================================================

function formatFileSize(
    bytes
) {

    if (bytes === 0) {
        return "0 Bytes";
    }


    const units = [
        "Bytes",
        "KB",
        "MB",
        "GB"
    ];


    const index =
        Math.floor(
            Math.log(bytes)
            /
            Math.log(1024)
        );


    return (
        parseFloat(
            (
                bytes
                /
                Math.pow(
                    1024,
                    index
                )
            ).toFixed(2)
        )
        +
        " "
        +
        units[index]
    );

}


function delay(ms) {

    return new Promise(
        resolve =>
            setTimeout(
                resolve,
                ms
            )
    );

}