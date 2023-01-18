#
# Makefile for diehard
#

CC=gcc

OBJS = diehard.o d3sphere.o kstest.o squeez.o cdbday.o cdosum.o df.o \
       mindist.o cdbinrnk.o cdpark.o cdoperm5.o cdbitst.o cnt1s.o \
       funct.o cdomso.o craptest.o runtest.o

CFLAGS = -Wno-format

diehard: $(OBJS)
	$(CC) -o diehard $(OBJS) -lm

diehard.o: diehard.c header.h macro.h
	$(CC) $(CFLAGS) -c diehard.c

d3sphere.o: d3sphere.c header.h macro.h
	$(CC) $(CFLAGS) -c d3sphere.c

kstest.o: kstest.c header.h macro.h	 
	$(CC) $(CFLAGS) -c kstest.c

cdoperm5.o: cdoperm5.c header.h
	$(CC) $(CFLAGS) -c cdoperm5.c

squeez.o: squeez.c header.h macro.h
	$(CC) $(CFLAGS) -c squeez.c

cdbday.o: cdbday.c header.h
	$(CC) $(CFLAGS) -c cdbday.c

cdosum.o: cdosum.c header.h
	$(CC) $(CFLAGS) -c cdosum.c

df.o: df.c 
	$(CC) $(CFLAGS) -c df.c

funct.o: funct.c macro.h
	$(CC) $(CFLAGS) -c funct.c

mindist.o: mindist.c header.h macro.h
	$(CC) $(CFLAGS) -c mindist.c

cdbinrnk.o: cdbinrnk.c header.h macro.h
	$(CC) $(CFLAGS) -c cdbinrnk.c

cdpark.o: cdpark.c header.h macro.h
	$(CC) $(CFLAGS) -c cdpark.c

cdbitst.o: cdbitst.c header.h
	$(CC) $(CFLAGS) -c cdbitst.c

cnt1s.o: cnt1s.c header.h
	$(CC) $(CFLAGS) -c cnt1s.c

cdomso.o: cdomso.c header.h
	$(CC) $(CFLAGS) -c cdomso.c

craptest.o: craptest.c header.h macro.h
	$(CC) $(CFLAGS) -c craptest.c
	
runtest.o: runtest.c header.h macro.h
	$(CC) $(CFLAGS) -c runtest.c
