from google.cloud import bigquery
import uuid
import urllib3


def upload_metrics_to_bq(test_name, total_time, epochs, batch_size,
    backend_type, backend_version, cpu_num_cores, cpu_memory, cpu_memory_info,
    platform_type, platform_machine_type, sample_type=None):

  #bigquery_client = bigquery.Client()
  # Explicitly use service account credentials by specifying the private key
  # file. All clients in google-cloud-python have this helper, see
  # https://google-cloud-python.readthedocs.io/en/latest/core/modules.html
  #   #google.cloud.client.Client.from_service_account_json

  bigquery_client = bigquery.Client.from_service_account_json('/usr/local/google/home/anjalisridhar/Downloads/Anj-Tf-8abadd6f416a.json')
  dataset = bigquery_client.dataset('keras_benchmarks')
  table = dataset.table('benchmarks')

  table.reload()

  query = """\
  INSERT keras_benchmarks.benchmarks (test_id,test_name,recorded_time,\
  metrics,keras_backend,cpu_info,platform_info) \
  VALUES(@testid,@testname,CURRENT_TIMESTAMP(),\
  (@metrics_totaltime,@metrics_epochs,@metrics_batch_size,@metrics_sampletype),\
  (@keras_backend_type, @keras_backend_version),\
  (@cpu_info_numcores,@cpu_info_memory, @cpu_info_memory_units),\
  (@platform_info_type,@platform_info_machine_type))
  """
  test_id = uuid.uuid4().int>>64
  print(test_id)
  query_job = bigquery_client.run_async_query(
      str(uuid.uuid4()),
      query,
      query_parameters=(
        bigquery.ScalarQueryParameter('testid', 'INTEGER', test_id),
        bigquery.ScalarQueryParameter('testname', 'STRING', test_name),
        bigquery.ScalarQueryParameter('metrics_totaltime', 'FLOAT', total_time),
        bigquery.ScalarQueryParameter('metrics_epochs', 'INTEGER', epochs),
        bigquery.ScalarQueryParameter('metrics_batch_size', 'INTEGER', batch_size),
        bigquery.ScalarQueryParameter('metrics_sampletype', 'STRING', sample_type),
        bigquery.ScalarQueryParameter('keras_backend_type', 'STRING', backend_type),
        bigquery.ScalarQueryParameter('keras_backend_version', 'STRING', backend_version),
        bigquery.ScalarQueryParameter('cpu_info_numcores', 'FLOAT', cpu_num_cores),
        bigquery.ScalarQueryParameter('cpu_info_memory', 'FLOAT', cpu_memory),
        bigquery.ScalarQueryParameter('cpu_info_memory_units', 'STRING', cpu_memory_info),
        bigquery.ScalarQueryParameter('platform_info_type', 'STRING', platform_type),
        bigquery.ScalarQueryParameter('platform_info_machine_type', 'STRING', platform_machine_type)))



  query_job.use_legacy_sql = False

  query_job.begin()
  query_job.result()  # Wait for job to complete.
