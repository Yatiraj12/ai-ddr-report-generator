async function generateDDR() {

const inspectionFile = document.getElementById("inspectionFile").files[0];
const thermalFile = document.getElementById("thermalFile").files[0];

if (!inspectionFile || !thermalFile) {
alert("Please upload both reports.");
return;
}

const formData = new FormData();
formData.append("inspection_report", inspectionFile);
formData.append("thermal_report", thermalFile);

const loading = document.getElementById("loading");
const reportSection = document.getElementById("reportSection");
const reportOutput = document.getElementById("reportOutput");

loading.classList.remove("hidden");
reportSection.classList.add("hidden");

try {

const response = await fetch("/generate-ddr", {
method: "POST",
body: formData
});

if (!response.ok) {
throw new Error("Server error");
}

const data = await response.json();

loading.classList.add("hidden");

reportSection.classList.remove("hidden");
reportOutput.textContent = data.report;

}
catch(error){

loading.classList.add("hidden");

alert("Error generating DDR report.");

console.error(error);

}

}