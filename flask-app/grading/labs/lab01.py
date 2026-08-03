def run_checks(connect, run_command):
    points = 0
    objectives = [{'objective': 'file_exists_in_evidence', 'points_possible': 3, 'points_earned': 0},
                  {'objective': 'file_has_ascii_art', 'points_possible': 3, 'points_earned': 0},
                  {'objective': 'new_index_exists', 'points_possible': 3, 'points_earned': 0},
                  {'objective': 'new_index_under_construction', 'points_possible': 3, 'points_earned': 0},
                  {'objective': 'index_does_not_contain_corrupt_file', 'points_possible': 4, 'points_earned': 0},
                  {'objective': 'apache_running', 'points_possible': 4, 'points_earned': 0}
                  ]
    result1 = result2 = result3 = result4 = result5 = result6 = ''

    server = connect('192.168.56.20')
    if server:
        result1 = run_command(server, 'ls /home/evidence/')
        result2 = run_command(server, 'grep -l "ALL YOUR BASE ARE BELONG TO US" /home/evidence/*')
        result3 = run_command(server, 'ls /var/www/html/index.html')
        result4 = run_command(server, 'grep -i "under construction" /var/www/html/index.html')
        result5 = run_command(server, 'grep -c "ALL YOUR BASE ARE BELONG TO US" /var/www/html/index.html')
        result6 = run_command(server, 'systemctl is-active httpd')
        server.close()

    if result1 != '':
        objectives[0].update({'points_earned': 3})

    if result2 != '':
        objectives[1].update({'points_earned': 3})

    if result3 != '':
        objectives[2].update({'points_earned': 3})

    if result4 != '':
        objectives[3].update({'points_earned': 3})

    if result5 == '0':
       objectives[4].update({'points_earned': 4})

    if result6 == 'active':
        objectives[5].update({'points_earned': 4})

    for objective in objectives:
        points += objective['points_earned']

        
    return points, objectives