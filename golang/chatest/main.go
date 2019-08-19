package main

import (
	"log"
	"net/http"
	"path/filepath"
	"sync"
	"text/template"
)

// single template
type templateHandler struct {
	once     sync.Once
	filename string
	templ    *template.Template
}

// HTTP Request serveHTTP handling
func (t *templateHandler) ServeHTTP(w http.ResponseWriter, r *http.Request) {
	t.once.Do(func() {
		t.templ = template.Must(template.ParseFiles(filepath.Join("templates", t.filename)))
	})
	t.templ.Execute(w, nil)
}

func main() {
	/*
	http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
		w.Write([]byte(`
			<html>
				<head>
				<title>ChaTest</title>
				</head>
				<body>
					test chat!!!
				</body>
			</html>
		`))
	})
	// start web server
	if err := http.ListenAndServe(":10000", nil); err != nil {
		log.Fatal("List and Serve: ", err)
	}
	*/
	//root
	http.Handle("/", &templateHandler{filename: "chat.html"})
	//start web server
	if err := http.ListenAndServe(":10000", nil); err != nil {
		log.Fatal("list and serve: ", err)
	}
}
