
document.addEventListener("DOMContentLoaded", function () {
  const tabla = document.getElementById("tabla-datos");
  if (tabla) {
    new DataTable(tabla, {
      paging: true,
      searching: true,
      ordering: true,
      pageLength: 10,
      language: { url: "https://cdn.datatables.net/plug-ins/1.13.6/i18n/es-ES.json" },
      order: [[1, "desc"]],
      responsive: true,
    });
  }

  const renderPlot = (jsonId, divId) => {
    const el = document.getElementById(jsonId);
    const target = document.getElementById(divId);
    if (!el || !target) return;
    const raw = (el.textContent || "").trim();
    if (!raw) {
      console.warn("Sin JSON para", divId);
      return;
    }
    try {
      const spec = JSON.parse(raw);
      Plotly.newPlot(target, spec.data, spec.layout, { displayModeBar: true, responsive: true });
    } catch (err) {
      console.error("Error renderizando", divId, err, "raw:", raw.slice(0, 200));
    }
  };

  renderPlot("data-frec", "chart-frec");
  renderPlot("data-tend", "chart-tend");
  renderPlot("data-dist", "chart-dist");

  const btnTop = document.getElementById("btn-top");
  if (btnTop) {
    btnTop.addEventListener("click", () => window.scrollTo({ top: 0, behavior: "smooth" }));
  }
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener("click", function (e) {
      e.preventDefault();
      const target = document.querySelector(this.getAttribute("href"));
      if (target) target.scrollIntoView({ behavior: "smooth", block: "start" });
    });
  });
});
