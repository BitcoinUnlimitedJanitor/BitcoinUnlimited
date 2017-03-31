import pdb
import sys

TAB_SIZE = 8

def main(files, cutoff,verbose=False):
    for f in files:
        changed = False
        if verbose:
            print("Processing %s" % f)
        fo = open(f,"r")
        lines = fo.readlines()
        output = []
        for line in lines:
            #print len(line), "//" in line, line
            line = line.replace("\t",TAB_SIZE*" ")
            if len(line) > cutoff and "//" in line:
                try:
                    (code, comment) = line.rsplit("//",1)
                except ValueError:
                    print line
                    pdb.set_trace()
                # If there is a quote both the code and the comment, the // is likely in a comment    
                if comment.count('"')%2==1 and code.count('"')%2==1:
                    print("Warning, this line is weird, not touching...")
                    print(line)
                    output.append(line)
                    continue
                codeLen = len(code.lstrip())
                indentation = len(code) - codeLen
                if codeLen: # trailing comments has at least some code on the line
                    # pdb.set_trace()
                    newComment = " "*indentation + "//" + comment
                    if verbose:
                        print("Was:\n%s" % line.rstrip())
                        print("Now:")
                        print(newComment.rstrip())
                        print(code.rstrip())
                        #sys.stdout.write(newComment)
                        #sys.stdout.write(code)
                    output.append(newComment)
                    output.append(code.rstrip() + "\n")
                    changed = True
                else:
                    output.append(line)
            else:
                output.append(line)
        if changed:
            print("%s changed" % f)        
            fo = open(f,"w")
            fo.writelines(output)


if __name__ == '__main__':
    main(sys.argv[2:],int(sys.argv[1]))
