# --- PARAMETER FILE ---

# --- Start date. Use in first start and value error in check file
p_start_date = '2016-01-01 00:00:00'

# --- System OGG Log ---
p_system_log = '/oracle/ogg12/ggserr.log'

# --- Log File ---
p_logfile = 'files/ggserr.log'

# --- Number of last lines from system log, use in command "tail". Sample p_tail_number = 500000 ---
p_tail_number = 500000

# --- Check File ---
p_checkfile = '/oracle/send_ogg_error/files/check'

# --- Path to system OGG directory dirrpt. Use if need detailed log file
p_dirrpt = '/oracle/ogg12/dirrpt/'

# --- Temp directory. Use for create zip report file and further attach detailed log file
p_temp_dir = '/tmp/'

# --- Post configuration ---
p_smtp_server = 'smtp.example.ru'
p_send_from = 'OGGERR@mail.example.ru'
p_send_to = ['user@example.ru']
p_mail_subject = 'An ERROR on the server replication OGG'

# --- Send report file in attach email (False or True)
p_send_report = False

#--- Use advanced mail subject (False or True)
p_print_as_name = True

# --- Dictionary of replications ---
p_dict_replications = {
    'REPLICAT1'     : 'System 1',
    'REPLICAT2'     : 'System 2',
    'REPLICAT3'     : 'System 3'
}


