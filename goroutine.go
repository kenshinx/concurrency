package main

import (
	"errors"
	"fmt"
	"io/ioutil"
	"net/http"
	"regexp"
	"time"
)

var hosts = []string{
	"http://www.baidu.com",
	"http://www.amazon.com",
	"http://www.ibm.com",
	"http://www.python.org",
	"http://www.microsoft.com",
}

func Read(host string, ch chan int) {
	resp, err := http.Get(host)
	if err != nil {
		fmt.Errorf("%s http request failed", host)
		return
	}
	defer func() {
		ch <- 1
		resp.Body.Close()
	}()

	body, _ := ioutil.ReadAll(resp.Body)

	title, err := extractTitle(string(body))

	if err != nil {
		fmt.Errorf("%s get title failed", host)
		return
	}

	fmt.Printf("%s : %s\n", host, title)

}

func extractTitle(html string) (title string, err error) {
	defer func() {
		if r := recover(); r != nil {
			err = errors.New("Extract Title error")
		}
	}()
	r, _ := regexp.Compile("<title>(.+)</title>")
	title = r.FindStringSubmatch(html)[1]
	return

}

func main() {

	start := time.Now()

	chs := make([]chan int, 150)

	j := 0
	for i := 0; i < 30; i++ {
		for _, host := range hosts {
			chs[j] = make(chan int)
			go Read(host, chs[j])
			j++
		}
	}

	for _, ch := range chs {
		<-ch
	}

	end := time.Now()

	fmt.Printf("Elapsed Time : %f\n", end.Sub(start).Seconds())

}
