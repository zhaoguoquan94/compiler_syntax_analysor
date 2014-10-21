#coding:utf-8
import re

def main():
	a = re.findall(r'(?<=[\[]).*?(?=[\]])|(?<=[<]).*?(?=[>])', '<N>	->	[a][[]<n>[]]<p>')
	print(a)
	# print(a[1,len(a)])
	# a = [1,2,3]
	# print(a[1:len(a)])


if __name__ == '__main__':
	main()