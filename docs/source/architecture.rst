Architecture
============

The project separates UI code from reusable analysis and modelling code.

High-Level Structure
--------------------

.. code-block:: text

   Streamlit UI
       |
       v
   pages/
       |
       v
   src/utils and src/models
       |
       v
   AirQualityUCI dataset

Core Modules
------------

``src.utils.data_loader``
   Loads the original dataset, parses timestamps, handles decimal commas, and converts ``-200`` sentinels to missing values.

``src.utils.preprocessing``
   Builds temporal features and leakage-aware modelling frames.

``src.utils.analysis``
   Provides summary statistics, variable type summaries, correlations, p-values, adjacency matrices, and network edge lists.

``src.utils.metadata``
   Provides a human-readable data dictionary.

``src.models.regression``
   Defines regression pipelines and model evaluation.

Dashboard Pages
---------------

``app.py``
   Home page and project overview.

``pages/1_Data_Overview.py``
   Dataset profile, missing values, variable types, and descriptive statistics.

``pages/2_Sensor_Analysis.py``
   Sensor/reference relationships, correlation matrices, p-values, adjacency matrices, and network graph.

``pages/3_Modeling.py``
   Regression benchmark interface.

``pages/4_Scientific_Notes.py``
   Scientific assumptions, model methods, limitations, and possible extensions.
