import os
import sys

def usage():
    print('%s all     -- build all bsp' % os.path.basename(sys.argv[0]))
    print('%s clean   -- clean all bsp' % os.path.basename(sys.argv[0]))
    print('%s update  -- update all prject files' % os.path.basename(sys.argv[0]))
#找到bsp
BSP_ROOT = os.path.join("..", "..", "bsp")

if len(sys.argv) != 2:
    usage()
    sys.exit(0)
#更新MDK等文件
def update_project_file(project_dir):
    if os.path.isfile(os.path.join(project_dir, 'template.Uv2')):
        print('prepare MDK3 project file on ' + project_dir)
        command = ' --target=mdk -s'
        os.system('scons --directory=' + project_dir + command + ' > 1.txt')

    if os.path.isfile(os.path.join(project_dir, 'template.uvproj')):
        print('prepare MDK4 project file on ' + project_dir)
        command = ' --target=mdk4 -s'
        os.system('scons --directory=' + project_dir + command + ' > 1.txt')

    if os.path.isfile(os.path.join(project_dir, 'template.uvprojx')):
        print('prepare MDK5 project file on ' + project_dir)
        command = ' --target=mdk5 -s'
        os.system('scons --directory=' + project_dir + command + ' > 1.txt')

    if os.path.isfile(os.path.join(project_dir, 'template.ewp')):
        print('prepare IAR project file on ' + project_dir)
        command = ' --target=iar -s'
        os.system('scons --directory=' + project_dir + command + ' > 1.txt')

#更新所有文件夹文件，先执行menuconfig --silent 再执行scons
#处理带有sconstruct的文件夹
def update_all_project_files(sconstruct_paths):
    for projects in sconstruct_paths:
        print('==update=======projects='+ projects)
        try:
            # update rtconfig.h and .config
            if os.path.isfile(os.path.join(projects, 'Kconfig')):
                print('==11111=')
                if "win32" in sys.platform:
                    retval = os.getcwd()
                    os.chdir(projects)
                    os.system("menuconfig --silent")
                    os.chdir(retval)
                else:
                    os.system('scons --pyconfig-silent -C {0}'.format(projects))
                print('==menuconfig=======projects='+ projects)

            else:
                print('==no kconfig=in==!!!!!=projects='+ projects)
            # update mdk, IAR etc file
            update_project_file(projects)
        except Exception as e:
            print("error message: {}".format(e))
            sys.exit(-1)

#找到带有Sconstruct的文件夹
def find_sconstruct_paths(project_dir, exclude_paths):
    sconstruct_paths = []
    for root, dirs, files in os.walk(project_dir):
        if all(exclude_path not in root for exclude_path in exclude_paths):
            if 'SConstruct' in files:
                sconstruct_paths.append(root)
    return sconstruct_paths

exclude_paths = ['templates', 'doc']
sconstruct_paths = find_sconstruct_paths(BSP_ROOT, exclude_paths)

# get command options
command = ''
# 只执行scons
if sys.argv[1] == 'all':
    command = ' '
elif sys.argv[1] == 'clean':
    command = ' -c'
    print('begin to clean all the bsp projects')
# 执行所有其他IDE的update 但是不编译,这个一般不会出错
elif sys.argv[1] == 'update':
    print('begin to update all the bsp projects')

#更新所有的工程
    update_all_project_files(sconstruct_paths)

    print('finished!')
    sys.exit(0)
else:
    usage()
    sys.exit(0)





if sconstruct_paths:
    print("包含 'SConstruct' 文件的路径:")
    for path in sconstruct_paths:
        print(path)
else:
    print("未找到包含 'SConstruct' 文件的路径")
for project_dir in sconstruct_paths:
    print('=========project_dir='+ project_dir)
#判断有没有SConstruct 文件，
    if os.path.isfile(os.path.join(project_dir, 'SConstruct')):
#这里只编译了gcc 其他IAR 等没有进行编译
#判断一下cmd中的ide=mdk4
        print('=========begin to build bsp '+project_dir)
        if os.system('scons --directory=' + project_dir + command) != 0:
            print('build failed!!')
            break
    elif os.path.isfile(os.path.join(project_dir, item +'SConstruct')):
        print('!!!!!=begin to build bsp '+project_dir)
