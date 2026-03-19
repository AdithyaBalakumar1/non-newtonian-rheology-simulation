"""Markdown report generator."""
import datetime
import shutil
from pathlib import Path
from typing import Dict, Optional, List


def generate_report(
    run_id: str,
    model_results: Dict,
    pipe_flow_results: List,
    fit_results: Optional[Dict],
    plot_paths: List[str],
    output_dir: str = "results",
) -> str:
    """
    Generate a Markdown report with key results.

    Parameters
    ----------
    run_id : str
        Unique run identifier.
    model_results : dict
        Rheology model scalar results.
    pipe_flow_results : list
        List of PipeFlowResults.
    fit_results : dict or None
        Model fitting results.
    plot_paths : list
        Paths to saved plot files.
    output_dir : str
        Base output directory.

    Returns
    -------
    str path to generated report.
    """
    out_dir = Path(output_dir) / run_id
    out_dir.mkdir(parents=True, exist_ok=True)

    for p in plot_paths:
        src = Path(p)
        if src.exists():
            shutil.copy(src, out_dir / src.name)

    lines = [
        "# Non-Newtonian Rheology Simulation Report",
        "",
        f"**Run ID:** `{run_id}`  ",
        f"**Generated:** {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "",
        "---",
        "",
        "## Rheology Models",
        "",
    ]

    for model_name, scalars in model_results.items():
        lines.append(f"### {model_name}")
        for k, v in scalars.items():
            lines.append(f"- **{k}**: {v}")
        lines.append("")

    if pipe_flow_results:
        lines += ["## Steady Pipe Flow Results", ""]
        for res in pipe_flow_results:
            lines.append(f"### {res.model_name}")
            lines.append(f"- **Wall shear stress τ_w**: {res.tau_w:.4f} Pa")
            lines.append(f"- **Volumetric flow rate Q**: {res.Q:.6e} m³/s")
            lines.append(f"- **Average velocity V**: {res.V_avg:.6f} m/s")
            if res.r_p is not None:
                lines.append(f"- **Plug radius r_p**: {res.r_p:.6f} m")
            if res.Re_g is not None:
                lines.append(f"- **Generalized Reynolds number Re_g**: {res.Re_g:.2f}")
            lines.append("")

    if fit_results:
        lines += ["## Parameter Fitting Results", ""]
        for key, res in fit_results.items():
            if "error" in res:
                lines.append(f"### {key}: ERROR — {res['error']}")
            else:
                lines.append(f"### {res['model']}")
                for pname, pval in res["params"].items():
                    lines.append(f"- **{pname}**: {pval:.6f}")
                lines.append(f"- **RMSE**: {res['rmse']:.6f}")
                lines.append(f"- **R²**: {res['r2']:.6f}")
                lines.append(f"- **AIC**: {res['aic']:.4f}")
                lines.append(f"- **BIC**: {res['bic']:.4f}")
            lines.append("")

    if plot_paths:
        lines += ["## Plots", ""]
        for p in plot_paths:
            fname = Path(p).name
            lines.append(f"![{fname}]({fname})")
            lines.append("")

    report_path = out_dir / "report.md"
    report_path.write_text("\n".join(lines))
    print(f"Report saved to: {report_path}")
    return str(report_path)
