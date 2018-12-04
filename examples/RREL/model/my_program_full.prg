import "my_classes.def"

obj a0 : A
obj b0 : B
obj a1 : p1.A
obj b1:  p1.B
obj c1:  p1.C
obj a2 : p1.p2.A
obj b2:  p1.p2.B
obj c2:  p1.p2.C

// level0
call a0.alevel0
call b0.blevel0

// level1
call a1.alevel1
call b1.blevel1
call c1.clevel1

// level1+inh
call b1.blevel2
call c1.clevel2
call c1.blevel1
call c1.blevel2

// level2
call a2.alevel2
call b2.blevel2
call c2.clevel2
