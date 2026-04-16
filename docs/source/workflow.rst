Development Workflow
====================

This page summarizes the development workflow. The canonical Markdown version is available at ``docs/WORKFLOW.md``.

Environment
-----------

Create a virtual environment and install dependencies:

.. code-block:: powershell

   python -m venv venv
   venv\Scripts\activate
   python -m pip install --upgrade pip
   pip install -r requirements.txt

Run the dashboard:

.. code-block:: powershell

   streamlit run app.py

Run tests:

.. code-block:: powershell

   pytest tests -p no:cacheprovider

Data Rules
----------

The original CSV uses semicolon separators, decimal commas, and ``-200`` as the missing-value sentinel. The project converts ``-200`` into ``NaN`` during loading.

Model Rules
-----------

The modelling task is regression. The project uses chronological holdout evaluation, time-series cross-validation, and regression metrics such as MAE, RMSE, and R2.

Scientific Constraints
----------------------

The dashboard does not certify air quality and does not provide a production monitoring system. It is a reproducible baseline for analysing noisy historical sensor data.
