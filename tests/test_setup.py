import sys, os
current_dir = os.path.dirname(__file__)
src_dir = os.path.join(current_dir, '..', 'src')
sys.path.append(os.path.abspath(src_dir))