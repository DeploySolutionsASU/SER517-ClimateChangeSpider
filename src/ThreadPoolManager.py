import concurrent.futures


def start_job(all_data, func, thread_count):
    with concurrent.futures.ThreadPoolExecutor(max_workers=thread_count) as executor:

        future_to_guid = {executor.submit(func, guid, all_data[guid]): guid for guid in all_data.keys()}

        for future in concurrent.futures.as_completed(future_to_guid):
            guid = future_to_guid[future]
            try:
                data = future.result()
            except Exception as exc:
                print('%r generated an exception: %s' % (guid, exc))
            else:
                print(guid, "->", data)
