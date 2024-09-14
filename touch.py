{
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# Stock Price Prediction Pipeline with Apache Airflow and GitHub README Update\n",
    "In this notebook, I will demonstrate how to orchestrate a pipeline using Apache Airflow to generate predicted vs actual stock prices, update a README file on a GitHub repository with the latest plot, and push changes to GitHub automatically every day.\n",
    "\n",
    "This setup involves three main steps:\n",
    "1. **Data Ingestion and Preparation**: Ingest and prepare stock price data for prediction.\n",
    "2. **Plot Generation**: Use the prepared data to generate a daily plot of predicted vs actual stock prices using a Python script (`plot.py`).\n",
    "3. **README Update**: Update the README file in the GitHub repository with the latest plot and push the changes to GitHub."
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 1. Data Ingestion and Preparation\n",
    "The first step of the pipeline is to ingest daily stock price data and prepare it for the prediction task.\n",
    "In this case, the data is updated daily using Airflow and is passed to the `plot.py` function for generating the plot.\n",
    "\n",
    "```python\n",
    "def update_data():\n",
    "    \"\"\"Update stock price data (this is an example function, replace with your data update logic)\"\"\"\n",
    "    # Your data update logic here\n",
    "    pass\n",
    "```\n",
    "The `update_data` function can be replaced with any data ingestion logic that updates the stock price data daily. This is orchestrated via Airflow."
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 2. Plot Generation\n",
    "Once the data has been updated, the next step is to generate the plot that compares predicted and actual stock prices.\n",
    "\n",
    "This is handled by the `plot.py` function, which performs the heavy lifting. Here’s an example of how you can call the script using Airflow:\n",
    "\n",
    "```python\n",
    "def update_plot():\n",
    "    \"\"\"Run the plot generation script\"\"\"\n",
    "    os.system(\"python /path_to_your_repo/plot.py\")\n",
    "```\n",
    "This script generates a new plot daily using the most recent data, and the plot is saved in the repository as `latest_plot.png`."
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 3. README Update and GitHub Push\n",
    "Once the plot is generated, we automate the process of updating the README file and pushing the changes to the GitHub repository.\n",
    "\n",
    "### Steps for GitHub Update\n",
    "1. Append the latest plot image to the README file.\n",
    "2. Use Git to commit the changes.\n",
    "3. Push the changes to the GitHub repository.\n",
    "\n",
    "Here’s the Python function that handles the README update and GitHub push:\n",
    "\n",
    "```python\n",
    "def update_readme():\n",
    "    \"\"\"Update the README file with the new plot link and commit changes\"\"\"\n",
    "    readme_path = \"/path_to_your_repo/README.md\"\n",
    "    \n",
    "    # Update the README content (you can add the latest plot or other info)\n",
    "    with open(readme_path, \"a\") as readme_file:\n",
    "        readme_file.write(f\"![Latest Plot](./latest_plot.png)\\n\")\n",
    "    \n",
    "    # Commit and push changes to GitHub\n",
    "    repo_path = \"/path_to_your_repo/\"\n",
    "    subprocess.run([\"git\", \"add\", \"README.md\"], cwd=repo_path)\n",
    "    subprocess.run([\"git\", \"commit\", \"-m\", \"Updated README with latest plot\"], cwd=repo_path)\n",
    "    subprocess.run([\"git\", \"push\", \"origin\", \"main\"], cwd=repo_path)\n",
    "```\n",
    "This ensures that the README file is updated with the latest plot every day, and the changes are pushed to the GitHub repository."
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 4. Integrating the Steps into a Main Airflow DAG\n",
    "Finally, we integrate the above steps into the main DAG using Apache Airflow. The DAG will orchestrate the entire pipeline by defining the dependencies between tasks and ensuring they run sequentially.\n",
    "\n",
    "Here’s an example DAG that integrates data ingestion, plot generation, and README update:\n",
    "\n",
    "```python\n",
    "from airflow import DAG\n",
    "from airflow.operators.python_operator import PythonOperator\n",
    "from airflow.utils.dates import days_ago\n",
    "import subprocess\n",
    "import os\n",
    "\n",
    "default_args = {\n",
    "    'owner': 'airflow',\n",
    "    'depends_on_past': False,\n",
    "    'email_on_failure': False,\n",
    "    'email_on_retry': False,\n",
    "    'retries': 1,\n",
    "}\n",
    "\n",
    "dag = DAG(\n",
    "    'main_stock_price_dag',\n",
    "    default_args=default_args,\n",
    "    description='Daily stock price DAG with README update',\n",
    "    schedule_interval='@daily',\n",
    "    start_date=days_ago(1),\n",
    ")\n",
    "\n",
    "# Task to update data (from your existing DAG)\n",
    "update_data_task = PythonOperator(\n",
    "    task_id='update_data',\n",
    "    python_callable=update_data,\n",
    "    dag=dag,\n",
    ")\n",
    "\n",
    "# Task to generate the plot\n",
    "generate_plot_task = PythonOperator(\n",
    "    task_id='generate_plot',\n",
    "    python_callable=update_plot,\n",
    "    dag=dag,\n",
    ")\n",
    "\n",
    "# Task to update the README and push changes\n",
    "update_readme_task = PythonOperator(\n",
    "    task_id='update_readme',\n",
    "    python_callable=update_readme,\n",
    "    dag=dag,\n",
    ")\n",
    "\n",
    "# Set the task dependencies\n",
    "update_data_task >> generate_plot_task >> update_readme_task\n",
    "```"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Conclusion\n",
    "This setup shows how Apache Airflow can be used to orchestrate a stock price prediction pipeline, generate a daily plot, and automatically update a GitHub README file. The automation ensures that the repository remains up to date with the latest stock price data and visualizations, providing a continuous and reliable process for maintaining the project."
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "name": "python",
   "version": "3.8.5"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
