"""Website Director Browser & Regression QA subsystem (V2.8).

The canonical *policy* lives in ``BROWSER-REGRESSION-QA-PROTOCOL.md``.
This package is the reusable *harness*: replaceable browser-execution engines
(``engine/``), requirement-traced assertion modules (``assertions/``), the
frozen-project integrity guard (``guards/``), and the manifest-driven runner
(``runner.py``). Engines are swappable; the policy is not.
"""

__version__ = "2.8.0"
