# coding=utf-8

import asyncio
        import concurrent.futures
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        async def run_my_functions():
            with concurrent.futures.ThreadPoolExecutor() as executor:
                c_all_task = list()
                for deployinfo in l_deployinfo:
                    name = deployinfo.get('Key', '')
                    if name == 'guard':
                        result_device = loop.run_in_executor(executor, exec_one_config, deployinfo, 'device')
                        c_all_task.append(result_device)
                        result_nginx = loop.run_in_executor(executor, exec_one_config, deployinfo, 'nginx')
                        c_all_task.append(result_nginx)
                        result_haproxy = loop.run_in_executor(executor, exec_one_config, deployinfo, 'haproxy')
                        c_all_task.append(result_haproxy)
                        l_deployinfo.remove(deployinfo)
                        break
                for deployinfo in l_deployinfo:
                    result = loop.run_in_executor(executor, exec_one_config, deployinfo)
                    c_all_task.append(result)

                results = await asyncio.gather(*c_all_task)
                # print(results)

        loop.run_until_complete(run_my_functions())

        loop.close()

