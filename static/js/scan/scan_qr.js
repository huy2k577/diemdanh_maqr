let html5QrCode = null;
let isScanning = false;
let lastScannedText = "";
let lastScanTime = 0;

const startBtn = document.getElementById("start-camera-btn");
const stopBtn = document.getElementById("stop-camera-btn");
const resultBox = document.getElementById("scan-result");

function renderResult(message, isSuccess = true) {
    resultBox.innerHTML = `
        <div class="${isSuccess ? 'result-success' : 'result-error'}">
            ${message}
        </div>
    `;
}

async function saveScanResult(qrText) {
    const response = await fetch(window.SCAN_CONFIG.saveUrl, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": window.SCAN_CONFIG.csrfToken
        },
        body: JSON.stringify({ qr_text: qrText })
    });

    const data = await response.json();
    return { ok: response.ok, data };
}

async function stopScanner() {
    if (html5QrCode && isScanning) {
        try {
            await html5QrCode.stop();
            await html5QrCode.clear();
        } catch (error) {
            console.error(error);
        }

        isScanning = false;
        startBtn.style.display = "inline-flex";
        stopBtn.style.display = "none";
    }
}

async function onScanSuccess(decodedText) {
    const now = Date.now();

    // chống spam quét 1 mã nhiều lần liên tục
    if (decodedText === lastScannedText && now - lastScanTime < 2000) {
        return;
    }

    lastScannedText = decodedText;
    lastScanTime = now;

    try {
        const result = await saveScanResult(decodedText);

        if (result.ok && result.data.success) {
            const sv = result.data.student;

            renderResult(`
                <strong>Quét thành công</strong><br>
                Mã SV: ${sv.masv}<br>
                Tên SV: ${sv.tensv}<br>
                Năm sinh: ${sv.namsinhsv}
            `, true);

         
        } else {
            renderResult(result.data.message, false);
        }

    } catch (error) {
        console.error(error);
        renderResult("Lỗi khi gửi dữ liệu.", false);
    }
}

startBtn.addEventListener("click", async function () {
    if (isScanning) return;

    html5QrCode = new Html5Qrcode("reader");

    try {
        await html5QrCode.start(
            { facingMode: "environment" },
            {
                fps: 10,
                qrbox: { width: 350, height: 350 }
            },
            onScanSuccess
        );

        isScanning = true;
        startBtn.style.display = "none";
        stopBtn.style.display = "inline-flex";


    } catch (error) {
        console.error(error);
        renderResult("Không bật được camera.", false);
    }
});

stopBtn.addEventListener("click", async function () {
    await stopScanner();
    renderResult("Camera đã tắt.", true);
});