from __future__ import print_function
import json
import os
import requests
import commands
from bs4 import BeautifulSoup
import re
import getopt
import sys
import string
import random
import print_table as table
import check_linux as chenkU


# Check Official Image
def official_image(i_name):
    url = 'https://github.com/docker-library/official-images/tree/master/library/' + i_name
    response = requests.get(url)

    if response.status_code == 200:
        return True
    
    else:
        return False

# Find Compose File by Image name
def find_compose(image_name):
    cmd = commands.getoutput(
        'find / -name ' + image_name + ' 2> /dev/null').split('\n')

    if cmd[0] == '':
        return False

    while True:
        for i in range(len(cmd)):
            num = i + 1
            print('%d. %s' %(num, cmd[i]))

        select = int(input('Enter number of your path : '))

        if select > (len(cmd) + 1) or select <= 0:
            print('You Choose Wrong Number. Try again.\n')
            continue

        return cmd[select - 1]

# Find Service & Version in Image name
def findVer_image(compose_path): 
    cmd = commands.getoutput('grep image ' + compose_path)
    images= cmd.replace('image: ', '').split('\n')
    
    services = dict()

    if cmd=='':
        return False

    for image in images:
        i_name = ''
        i_ver = ''
        image = image.replace(' ', '')

        if ':' in image :
            i_name = image.split(':')[0]
            i_ver = image.split(':')[1]
            services[i_name] = i_ver

        if i_ver == 'latest' or ':' not in image:
            i_name = image
            i_ver = 'latest'
                    
            url = 'https://github.com/docker-library/official-images/tree/master/library/' + i_name
            response = requests.get(url)

            if response.status_code == 200 :
                html = response.text
                soup = BeautifulSoup(html, 'html.parser')
                target = soup.find('table', {'class':'highlight tab-size js-file-line-container'}).get_text().split('\n')
                tags = []

                for line in target:
                    if i_ver in line :
                        line = str(line)
                        tags = line.replace('Tags:', '')
                        tags = tags.replace(' ', '')
                        tags = tags.split(',')
                        tags.remove('latest')
                        i_ver = tags[0]
                        services[i_name] = i_ver
                        break
                            
    return services    

# Find Service & Version in Package.json
def findVer_package(dir_path, compose_path):
    not_build = True
    
    if os.path.isfile(compose_path) == True:
        os.chdir(dir_path)
        cmd1=commands.getoutput('cat docker-compose.yaml').split('\n')
       

        for i in cmd1:
            if 'build' in i:
                build = i
                build = build.replace(' ', '')
                build = build.split(':')[1]
                not_build = False
                break
            else:
                not_build = True

    if not_build == False:
        os.chdir('{}'.format(build))
        json_path = os.getcwd()
        if os.path.isfile(json_path+'/package.json')==True:
            file = open('package.json')
            jsonString = json.load(file)
            services = dict()
            services_list=jsonString.get('dependencies').keys()
            for s in services_list :
                services[str(s)] = ''
 
            for s in services_list:
                str_s=str(s)
                tmp=jsonString['dependencies'][str_s].replace('^','')
                services[s] = str(tmp)
     
            if len(services)>0:
                return services

        else:
            return False
            

    elif not_build == True:
        return False

# Find Service & Version in env file
def findVer_env(dir_path, compose_path):
    env_path = dir_path + '/.env'

    cmd1 = commands.getoutput('grep -n build ' + compose_path).split('\n')
    cmd2 = commands.getoutput("grep '\$' " + compose_path).split('\n')
    
    if cmd2[0] == '':
        return False

    services = dict()

    for c in cmd1:
        if c != '':
            service_line = int(c.split(':')[0]) - 1
            service_name = cmd1 = os.popen(
                'sed -n ' + str(service_line) + 'p ' + compose_path).read().split(':')[0].lstrip()
            services[service_name] = ''

    variables = dict()

    for c, service in zip(cmd2, services) :
        if c != '':
            variables[c.split('$')[1]] = 'none'
            services[service] = c.split('$')[1]    

    cmd3 =  commands.getoutput('cat ' + env_path).split('\n')
    for c in cmd3:
        if c != '':
            var_name = c.split('=')[0]
            var_value = c.split('=')[1]
            variables[var_name] = var_value

    for service in services:
        val = services[service]
        services[service] = variables[val]

    return services

# Find Service & Version in Dockerfile
def findVer_dockerfile(dir_path, compose_path):
    cmd1 = commands.getoutput('grep -n build ' + compose_path).split('\n')
    
    if cmd1[0] == '' :
        return False

    services = dict()

    for c in cmd1 :
        service_name = c.replace(' ', '').split(':')[2]
        dockerfile_path = dir_path + '/' +  service_name + 'Dockerfile'

        cmd2 = commands.getoutput('grep FROM ' + dockerfile_path).split('\n')
     
        if 'No such file' in cmd2[0] :
            return False 

        for c in cmd2 : 
            d_service = c.split(' ')[1].replace(':',' ').split('-')[0]
            d_service_name = d_service.split(' ')[0]
            d_service_ver = d_service.split(' ')[1]
            services[d_service_name] = d_service_ver

    return services

# Get Vulnerability by Service name without Version
def default_exploit(service):
    title = []
    url = []
    url_list = []
    title_list = []
    cve_list = []
    length_of_string = 8
    filename = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length_of_string))+'.json'
    cmd1 = commands.getoutput('searchsploit -jtw ' + service + ' > ' + filename)
    file = open(filename)
    jsonObject = json.load(file)
    result = jsonObject.get("RESULTS_EXPLOIT")

    for list in result:
        title.append(list.get("Title"))
        url.append(list.get("URL"))

    os.remove(filename)

    v = re.compile('[0-9]')
    cnt = 0

    for i in title:
        cnt += 1
    
        if(str(i).split(" ")[0] == 'MySQL' or str(i).split(" ")[0] == 'Oracle') :
            if v.search(i) == None:
                title_list.append(i)
                url_only = url[cnt-1]
                url_list.append(url_only)

                try :
                    response = requests.get(url_only, headers={"User-Agent": "Mozilla/5.0"})

                    if response.status_code == 200 :
                        html = response.text
                        soup = BeautifulSoup(html, 'html.parser')
                        target = soup.find_all('div', {'class':'col-6 text-center'})

                        try :
                            cve = target[1].find('a', {'target':'_blank'}).text.strip()
                            cve_list.append(cve)

                        except :
                            cve_list.append("N/A")
                            
                except Exception as ex:
                    print(ex)
        else :
            if v.search(i) == None:
                title_list.append(i)
                url_only = url[cnt-1]
                url_list.append(url_only)

                try :
                    response = requests.get(url_only, headers={"User-Agent": "Mozilla/5.0"})

                    if response.status_code == 200 :
                        html = response.text
                        soup = BeautifulSoup(html, 'html.parser')
                        target = soup.find_all('div', {'class':'col-6 text-center'})

                        try :
                            cve = target[1].find('a', {'target':'_blank'}).text.strip()
                            cve_list.append(cve)

                        except :
                            cve_list.append("N/A")
                            
                except Exception as ex:
                    print(ex)

    return title_list, cve_list, url_list  

# Get Vulnerability by Service name with Version
def find_exploit(services):

    final_titles = []
    final_cve_list = []
    final_url_list = []   

    for service, version in services.items():  
        titles = []
        cve_list = []
        url_list = []     
        
        length_of_string = 8
        filename = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length_of_string))+'.json'
        cmd1 = commands.getoutput('searchsploit -jtw ' + service + ' > ' + filename)
        file = open(filename)
        jsonObject = json.load(file)
        result = jsonObject.get("RESULTS_EXPLOIT")
        default_titles, default_cves, default_url = default_exploit(service)
        os.remove(filename)
        
        
        for list in result:
            title = list.get("Title")
            url = list.get("URL")
            match = ' ' + str(version)
                        
            if(title.split(' ')[0].lower() == service and match in title) :
                titles.append(str(title))
                url_list.append(str(url))

                try :
                    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})

                    if response.status_code == 200 :
                        html = response.text
                        soup = BeautifulSoup(html, 'html.parser')
                        target = soup.find_all('div', {'class':'col-6 text-center'})

                        try :
                            cve = target[1].find('a', {'target':'_blank'}).text.strip()
                            cve_list.append(cve)

                        except :
                            cve_list.append("N/A")
                            
                except Exception as ex:
                    print(ex)
        
        titles = titles + default_titles
        cve_list = cve_list + default_cves
        url_list = url_list + default_url
    
        final_titles.append(titles)  
        final_cve_list.append(cve_list)
        final_url_list.append(url_list)

    return final_titles, final_cve_list, final_url_list


if __name__ == "__main__":
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'haosnctl', ['options'])
    except getopt.GetoptError as err:
        print(err)
        print('Usage : VulDock [OPTIONS] Image_name')
        print("Try 'VulDock -h' for more information")
        sys.exit()

    optCheck = 0

    if len(args) != 1 and ('-h', '') not in opts:
        print('\033[38;5;160m[ ERROR ]\033[0m Please Enter an Image name')
        print("'VulDock' requires exactly 1 argument.")
        print("See 'VulDock -h'")
        print('\nUsage : VulDock [OPTIONS] Image_name')
        sys.exit()

    elif ('-h', '') in opts:
        print('USAGE : VulDock [OPTIONS] Image_name \n' +
                'DESCRIPTION :\n' +
                '      -a\n' +
                '    show all options\n' +
                '      -t\n' +
                '    print CVE Title\n' +
                '      -c\n' +
                '    print CVE number\n' +
                '      -l\n' +
                '    print cve url\n' +
                '      -s\n' +
                '    print services list\n' +
                '      -n\n' +
                '    print the number of vulnerabilities\n' +
                '      -o\n' +
                '    print whether image is official or not\n')
        sys.exit()

    else:
        image_name = args[0]
        if opts == []:
            opts = [('-t', ''), ('-c', '')]
        
        
        dir_path = find_compose(image_name)
        compose_path = commands.getoutput('find ' + dir_path + ' -name docker-compose.y*') 

        if compose_path == '':
            print('\n\033[38;5;160m[ ERROR ]\033[0m Your Image is not a Type that Fits our Tool')
            sys.exit()

        services = dict()
        check_none_service = 0
        
        image_service = findVer_image(compose_path)
        if image_service != False:
            services.update(image_service)

        else:
            check_none_service += 1

        package_service = findVer_package(dir_path, compose_path)
        if package_service != False:
            services.update(package_service)
        
        else:
            check_none_service += 1

        env_service = findVer_env(dir_path, compose_path)
        if env_service != False:
            services.update(env_service)

        else:
            check_none_service += 1

        dockerfile_service = findVer_dockerfile(dir_path, compose_path)
        if dockerfile_service != False:
            services.update(dockerfile_service)
        
        else:
            check_none_service += 1
        
        if check_none_service == 4:
            print("\n\033[38;5;160m[ ERROR ]\033[0m You don't have any Service in Your Image")
            sys.exit()

        service_keys = services.keys()
        title_list = ['Title']
        cve_list = ['CVE']
        url_list = ['URL']
        execute = False
        chart_list = []

        if ('-a', '') in opts:
            opts = [('-o', ''), ('-s', ''), ('-n', ''), ('-t', ''), ('-c', ''), ('-l', '')]

        # Check Option
        for option, arg in opts:
            if '-o' == option:
                print('\n\033[48;5;7m\033[38;5;0m [ Check Official Image ] \033[0m')
                if image_service != False:
                    for service in image_service:
                        official = official_image(service)
                        
                        if official:
                            print(' > \033[38;5;178m%s\033[0m : Official Image' %service)
                        
                        else:
                            print(' > \033[38;5;178m%s\033[0m : Unofficial Image' %service)

                if package_service != False:
                    for service in package_service:
                        print(' > \033[38;5;178m%s\033[0m : Not Image' %service)

                if env_service != False:    
                    for service in env_service:
                        print(' > \033[38;5;178m%s\033[0m : Not Image' %service)
                
                if dockerfile_service != False:
                    for service in dockerfile_service:
                        official = official_image(service)
                        
                        if official:
                            print(' > \033[38;5;178m%s\033[0m : Official Image' %service)
                        
                        else:
                            print(' > \033[38;5;178m%s\033[0m : Unofficial Image' %service)

            
            elif '-s' == option:
                print('\n\033[48;5;7m\033[38;5;0m [ Service Version ] \033[0m')
                for service, version in services.items():
                    print(' > \033[38;5;178m%s\033[0m : %s' %(service, version))

            elif '-n' == option or '-t' == option or '-c' == option or '-l' == option:
                if execute == False:
                    find_titles, find_cves, find_urls = find_exploit(services)
                    title_list = title_list + find_titles
                    cve_list = cve_list + find_cves
                    url_list = url_list + find_urls
                    execute = True

                if '-n' == option:
                    print('\n\033[48;5;7m\033[38;5;0m [ The Number of Vulnerabilities by Service ] \033[0m')
                    vul_total = 0

                    for i in range(len(services)):
                        print(' > \033[38;5;178m%s\033[0m : %d' %(service_keys[i], len(find_titles[i])))
                        vul_total += len(find_titles[i])
                    
                    print(' > Total Vulnerability : %d\n' %vul_total)
                
                elif '-t' == option:
                    chart_list.append(title_list)
                    optCheck += 1
                            
                elif '-c' == option:
                    chart_list.append(cve_list)
                    optCheck += 1


                elif '-l' == option:
                    chart_list.append(url_list)
                    optCheck += 1

        if optCheck != 0:
            print('\n\033[48;5;7m\033[38;5;0m [ Vulnerabilities Chart ] \033[0m')

            for service_i in range(len(services)):
                print(' > Service name : \033[38;5;178m%s\033[0m' %service_keys[service_i])
                info_list = []

                for opt_i in range(optCheck):
                    service_list = []
                    service_list.insert(0, chart_list[opt_i][0])
                    
                    for title_i in range(len(chart_list[opt_i][service_i+1])):
                        service_list.insert(title_i+1, chart_list[opt_i][service_i + 1][title_i])
                        
                    info_list.append(service_list)

                table.print_table(info_list)
                print()

        # Check Linux OS
        linux_os = ['debian', 'linux' ,'ubuntu','redhat', 'kali' ,'fedora', 'centos']
        print('\n\033[48;5;7m\033[38;5;0m [ Linux OS Vulnerabilities Chart ] \033[0m')
        for key, value in services.items() :
            for linux_name in linux_os:
                if linux_name in key.lower():
                    result = chenkU.main_func(key, value, linux_name)
                    table.print_table(result)        