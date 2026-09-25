async function generateDocument() {

    const status = document.getElementById("status");
    const request = document.getElementById("request").value;

    if (request.trim() === "") {
        status.innerHTML = "Please enter a request.";
        return;
    }

    status.innerHTML = "🤖 Planning and generating document...";

    try {

        const response = await fetch("/generate-document", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                request: request
            })
        });

        if (!response.ok) {
            throw new Error("Failed to generate document.");
        }

        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);

        const a = document.createElement("a");
        a.href = url;

        const disposition = response.headers.get("Content-Disposition");
        let filename = "Generated_Document.docx";

        if (disposition && disposition.includes("filename=")) {
            filename = disposition
                .split("filename=")[1]
                .replace(/"/g, "");
        }

        a.download = filename;

        document.body.appendChild(a);
        a.click();
        a.remove();

        window.URL.revokeObjectURL(url);

        status.innerHTML = "✅ Document generated successfully!";

    }
    catch (error) {

        console.error(error);
        status.innerHTML = "❌ Failed to generate document.";

    }

}