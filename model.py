import os, smtplib, re, zipfile
from params import *
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from os.path import basename

class Parse():

    # ------ Constructor ------
    def __init__(self, logfile, checkfile):
        self.list = []
        self.file_send_list = []
        self.param_files_list = []
        self.full_as_list = []
        self.logpath = logfile
        self.checkpath = checkfile
        self._parse()

    # ------ Main function. Parse log file ------~~
    def _parse(self):
#        os.system('tail -' + str(p_tail_number) + ' ' + p_system_log + ' > ' + p_logfile)
        flog = open(self.logpath, 'r')
        for line in flog.readlines():
            try:
                type = line.split()[2]
                if type == 'ERROR' and self._check_last_date(line):
                    self.list.append(line)
                    self._find_file_in_string(line)
                    self._find_parameter_file_name(line)
            except IndexError:
                continue

        if self.list:
            if self.full_as_list and p_print_as_name:
                self.full_as_list.append('\n')
                self.list = self.full_as_list + self.list
            self._prepare_send_mail(self.list)

        self._print_result(self.list)
#        self._save_last_date(line)
        flog.close()

    # ------ Save date from last cheked string ------
    def _save_last_date(self, lstr):
        lastdate = lstr.split()[0] + ' ' + lstr.split()[1]
        fldata = open(self.checkpath, 'w')
        fldata.write(lastdate)
        fldata.close()

    # ------ Check new or old error ------
    def _check_last_date(self, errstr):
        #------ return saved date from file ------
        try:
            fcheck = open(self.checkpath, 'r')
        except FileNotFoundError:
            fcheck = open(self.checkpath, 'w+')
        saveddate = fcheck.readline()
        #------ If check file empty ------
        if not saveddate:
            saveddate = p_start_date
        #------ If date type not correct in check file run except ------
        try:
            datefromfile = self._str_to_date(saveddate)
        except ValueError:
            datefromfile = self._str_to_date(p_start_date)
        fcheck.close()

        #------ date Error current string ------
        strdate = errstr.split()[0] + ' ' + errstr.split()[1]
        dateerror = self._str_to_date(strdate)

        if dateerror > datefromfile:
            return True
        else:
            return

    # ------ Convert string to date ------
    def _str_to_date(self, str):
        date = datetime.strptime(str, '%Y-%m-%d %H:%M:%S')
        return date

    # ------ Print result parse log ------
    def _print_result(self, list):
        print('-------------------------------------------------------------------------------------------------------------------------')
        print('| Time of check log: ' + str(datetime.now()) + ' |')
        print('-------------------------------------------------')
        print('\n'.join(list))
        print('Result: find ' + str(len(list)) + ' error')

    # ------ Prepare send text ------
    def _prepare_send_mail(self, list):
        self._send_mail(list)

    # ------ Send mail ------
    def _send_mail(self, slist):
        msg_text = '\n'.join(slist)

        msg = MIMEMultipart(
            From=p_send_from,
            To=','.join(p_send_to),
            Subject=p_mail_subject
        )
        msg['Subject'] = p_mail_subject
        msg['From'] = p_send_from
        msg['To'] = ','.join(p_send_to)

        msg.attach(MIMEText(msg_text))

        # ------ Attach report file to email ------
        if self.file_send_list and p_send_report:
            for line in self.file_send_list:
                try:
                    report_file = line + '.rpt'
                    report_file_path = p_dirrpt + report_file
                    zip_file_path = p_temp_dir + line + '.zip'

                    # ------ Add report file in archive ------
                    zip_file = zipfile.ZipFile(zip_file_path, 'w', compression=zipfile.ZIP_DEFLATED)
                    zip_file.write(report_file_path, report_file)
                    zip_file.close()

                    with open(zip_file_path, 'rb') as fil:
                        msg.attach(MIMEApplication(
                            fil.read(),
                            Content_Disposition='attachment; filename="%s"' % basename(zip_file_path),
                            Name=basename(zip_file_path)
                            ))
                    print('File is attached to letter: ' + zip_file_path)
                except IOError:
                    print('No such file or directory: ' + line)
                except OSError:
                    print('No such file or directory: ' + line)

        try:
            s = smtplib.SMTP(p_smtp_server)
            s.sendmail(p_send_from, p_send_to, msg.as_string())
            s.quit()
            print('Successfully sent email')
        except:
            print('Error: unable to send email')

    # Find file for attach in string
    def _find_file_in_string(self, str):
        result = re.search(r'report\sfile\sof\s(.*?)\sfor', str)
        if result and not result.group(1) in self.file_send_list:
            self.file_send_list.append(result.group(1))

    # Find parameter file in string
    def _find_parameter_file_name(self, str):
        result = re.search(r'Delivery\sfor\sOracle,\s(.*?).prm:', str)
        if result and not result.group(1).upper() in self.param_files_list:
            self.param_files_list.append(result.group(1).upper())
            self._full_name_as(result.group(1))

    # Add full name replication in list
    def _full_name_as(self, str):
        try:
            full_name = (str.upper() + ' => ' + p_dict_replications[str.upper()])
        except:
            full_name = (str.upper() + ' => NONAME')
        self.full_as_list.append(full_name)
