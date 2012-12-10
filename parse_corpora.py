
import sys, re, os, glob
def new_doc_line(doc_line):
	p = re.compile("(SINO[\s]*)([\d]+)")
	r = p.search(doc_line)
	if r != None:
		return r.groups()[1]
	else:
		return False
		
def grab_segment(doc_line):
	p = re.compile('>(.*)<')
	r = p.search(doc_line)
	if r != None:
		return r.groups()[0]
	else:
		return False

def not_end_corp(doc_line):
	p = re.compile("/(\s*)(DOC)")
	r = p.search(doc_line)
	if r == None:
		return True
	else:
		return False

def not_end_ali(doc_line):
	doc_line = re.sub(r'\s', '', doc_line)
	if doc_line == "</ALIGNMENT>":
		return False
	else:
		return True

def get_sent_pair_ids(doc_line):
	p = re.compile("EnglishSegId= \"(.*)\" ChineseSegId= \"(.*)\" ")
	r = p.search(doc_line)
	eng = r.groups()[0].split(',')
	chi = r.groups()[1].split(',')
	if(eng[0] != '' and chi[0] != ''):
		eng = [int(s) for s in eng]
		chi = [int(s) for s in chi]
		return(eng,chi)
	return False

def create_docID_segments_dict(dfile):
	seg_dict = {}
	try:
		while 1:
			line = dfile.next()
			doc_id = new_doc_line(line)
			if doc_id:
				key = doc_id;
				values = []
				doc_line = dfile.next()
				while not_end_corp(doc_line):
					segment = grab_segment(doc_line)
					if segment:
						values.append(segment)
					doc_line = dfile.next()
				seg_dict[key] = values
	except StopIteration:
		return seg_dict
		pass

def get_sentence_pairs(alignment_file,segmented_chinese_file,english_file):
	# print "ALIGNMENT_FILE", alignment_file 
	# print "SEG_CHINESE_FILE", segmented_chinese_file 
	# print "ENGLISH_FILE", english_file
	alignments = open(alignment_file)
	f_chi = open(segmented_chinese_file)
	f_eng = open(english_file)
	chinese_segs = create_docID_segments_dict(f_chi)
	english_segs = create_docID_segments_dict(f_eng)
	chinese_sents = []
	english_sents = []
	try:
		while 1:
			line = alignments.next();
			#print "LINE", line
			doc_id = new_doc_line(line)
			if doc_id:
				key = doc_id;
				sent_pair = alignments.next();
				while not_end_ali(sent_pair):
					ids = get_sent_pair_ids(sent_pair)
					if ids:
						english_words = ""
						for e_id in ids[0]:
							english_words+=' '+english_segs[doc_id][e_id-1]
						for c_id in ids[1]:
							chinese_sents.append(chinese_segs[doc_id][c_id-1])
						for i in range(0,len(ids[1])):
							english_sents.append(english_words)
					sent_pair = alignments.next()
	except StopIteration:
		return (chinese_sents,english_sents)
		pass

def get_alignments(number_of_files, startidx=0):
	if number_of_files > 345:
		number_of_files = 345
	alignment_files = os.listdir("./alignment")
	chinese_files = os.listdir("./Chinese_seg")
	english_files = os.listdir("./English")
	chinese_sents = []
	english_sents = []
	for i in range(startidx,startidx+number_of_files):
		alignment_file = alignment_files[i]
		doc_id = new_doc_line(alignment_file)
		sentence_pairs = get_sentence_pairs("./alignment/"+alignment_file,"./Chinese_seg/SINO"+doc_id+".seg.txt","./English/SINO"+doc_id+".sgm")
		chinese_sents.extend(sentence_pairs[0])
		english_sents.extend(sentence_pairs[1])
	return (chinese_sents,english_sents)
