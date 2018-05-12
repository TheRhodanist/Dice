extern crate bufstream;

use std::str::FromStr;
use std::io::Write;
use std::net::{TcpListener, TcpStream};
use std::net::SocketAddr;
use std::thread::spawn;
use bufstream::BufStream;
use std::io::BufRead;
use std::sync::{Arc,RwLock};
use std::sync::mpsc;
use std::sync::mpsc::{Sender, Receiver};

fn handle_connection(stream: &mut BufStream<TcpStream>, chan: Sender<String>, arc: Arc<RwLock<Vec<String>>>) {
    let mut pos = 0;
    loop {
        {
            let lines = arc.read().unwrap();
            println!("DEBUG arc.read() => {:?}", lines);
            for i in pos..lines.len() {
                stream.write_fmt(format_args!("{}", lines[i])).unwrap();
                pos = lines.len();
            };
        }

        let mut reads = String::new();
        stream.read_line(&mut reads).unwrap();
        if reads.trim().len() != 0 {
            println!("DEBUG: reads len =>>>>> {}", reads.len());
            chan.send(reads).unwrap();
        }
    }
}

fn main() {
    let addr: SocketAddr = SocketAddr::from_str("127.0.0.1:11100").unwrap();
    let listener = TcpListener::bind(addr).unwrap();

    let (send, recv): (Sender<String>, Receiver<String>) = mpsc::channel();
    let arc: Arc<RwLock<Vec<String>>> = Arc::new(RwLock::new(Vec::new()));

    let arc_w = arc.clone();

    spawn(move|| {
        loop {
            let msg = recv.recv().unwrap();
            print!("DEBUG: msg {}", msg);
            {
                let mut arc_w = arc_w.write().unwrap();
                arc_w.push(msg);
            } // write lock is released at the end of this scope
        }
    });

    for stream in listener.incoming() {
        match stream {
            Err(_) => println!("listen error"),
            Ok(mut stream) => {
                println!("connection from {} to {}",
                         stream.peer_addr().unwrap(),
                         stream.local_addr().unwrap());
                let send = send.clone();
                let arc = arc.clone();
                spawn(move|| {
                    let mut stream = BufStream::new(stream);
                    handle_connection(&mut stream, send, arc);
                });
            }
        }
    }
}