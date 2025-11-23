import { downloadReportToBlob } from "../api/api";

export default function DownloadReport() {
  const handleDownload = async () => {
    try {
      const blob = await downloadReportToBlob();
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement("a");
      link.href = url;
      link.download = "latest_report.pdf";
      link.click();
      window.URL.revokeObjectURL(url);
    } catch {
      alert("Report download failed");
    }
  };

  return (
    <div>
      <h2>Download Latest Report</h2>
      <button onClick={handleDownload}>Download Report (PDF)</button>
    </div>
  );
}
