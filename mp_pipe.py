from multiprocessing import Pipe, Process


def f(conn):
  while True:
    val = conn.recv()
    if val is None:
      break
    conn.send(val * 2)

  conn.close()


if __name__ == '__main__':
  parent_conn, child_conn = Pipe()
  p = Process(target=f, args=(child_conn,))
  p.start()
  parent_conn.send(100)
  print(parent_conn.recv())
  parent_conn.send(None)
  p.join()
