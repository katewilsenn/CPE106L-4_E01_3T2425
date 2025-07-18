import sqlite3
import os
from clear import clearSYS

db_path = os.path.join(os.path.dirname(__file__), 'chinook.db')
LIMIT = 20

def searchTrackGenre() -> None:

	genre = input("Input Genre: ")
	with sqlite3.connect(db_path) as db:
		cursor = db.cursor()

		cursor.execute("""
		SELECT tracks.name, title, media_types.name, genres.name
		FROM tracks, albums, media_types, genres
		WHERE tracks.AlbumId = albums.AlbumId
		AND tracks.MediaTypeId = media_types.MediaTypeId
		AND tracks.GenreId = genres.GenreId 
		AND genres.name = ? LIMIT ?;
		""", (genre, LIMIT))

		results = cursor.fetchall()
		
		if not results:
			print(f"No tracks found for genre: {genre}")
			return

		border = 28
		print("-" * border)
		print("| TRACK-GENRE INFORMATION | ")
		print("-" * border, end = "\n\n")

		border = 150
		print("=" * border)
		print(f"{'Track':<40} {'Album':<60} {'Media Type':<30} {'Genre':<20}")
		print("=" * border)

		for res in results:
			print(f"{res[0]:<40} {res[1]:<60} {res[2]:<30} {res[3]:<20}")
		
		print("=" * border, end = "\n\n")

def printTrackBuyer() -> None:
	with sqlite3.connect(db_path) as db:
		cursor = db.cursor()
		
		cursor.execute("""
			SELECT tracks.name as track, customers.FirstName as name, invoice_items.UnitPrice, invoice_items.Quantity
			FROM tracks, customers, invoice_items, invoices
			WHERE invoice_items.TrackId = tracks.TrackId
			AND invoice_items.InvoiceId = invoices.InvoiceId
			AND invoices.CustomerId = customers.CustomerId
			LIMIT ?;
		""", (LIMIT,))

		results = cursor.fetchall()
		
		border = 27
		print("-" * border)
		print("| TRACK-BUYER INFORMATION | ")
		print("-" * border, end = "\n\n")

		border = 130
		print("=" * border)
		print(f"{'Track':<60} {'Buyer (FN)':<30} {'Unit Price':<20} {'Quantity':<20}")
		print("=" * border)

		for res in results:
			print(f"{res[0]:<60} {res[1]:<30} {res[2]:<20} {res[3]:<20}")
		
		print("=" * border, end = "\n\n")

def printTrackPlaylist() -> None:
	with sqlite3.connect(db_path) as db:
		cursor = db.cursor()
		
		cursor.execute("""
			SELECT DISTINCT tracks.name as track, playlists.name as playlist
			FROM tracks, invoice_items, invoices, playlists, playlist_track
			WHERE playlist_track.TrackId = invoice_items.TrackId
			AND invoice_items.TrackId = tracks.TrackId
			AND playlist_track.PlaylistId = playlists.PlaylistId
			LIMIT ?;
		""", (LIMIT,))

		results = cursor.fetchall()
		
		border = 30
		print("-" * border)
		print("| TRACK-PLAYLIST INFORMATION | ")
		print("-" * border, end = "\n\n")

		border = 80
		print("=" * border)
		print(f"{'Track':<50} {'Playlist':<30}")
		print("=" * border)

		for res in results:
			print(f"{res[0]:<50} {res[1]:<30}")
		
		print("=" * border, end = "\n\n")

def printTrackCustomer() -> None:
	with sqlite3.connect(db_path) as db:
		cursor = db.cursor()
		
		cursor.execute("""
			SELECT CONCAT(customers.FirstName, ' ', customers.LastName) AS name, tracks.name AS track, playlists.Name as playlist, CONCAT(employees.FirstName, ' ', employees.LastName) as supportRep, invoices.Total as total
			FROM customers, invoices, employees, tracks, playlist_track, invoice_items, playlists
			WHERE customers.CustomerId = invoices.CustomerId
			AND invoices.InvoiceId = invoice_items.InvoiceId
			AND tracks.TrackId = invoice_items.TrackId
			AND invoice_items.TrackId = playlist_track.TrackId
			AND customers.SupportRepId = employees.EmployeeId
			AND playlists.PlaylistId = playlist_track.PlaylistId
			LIMIT ?;
		""", (LIMIT, ))

		results = cursor.fetchall()
		
		border = 30
		print("-" * border)
		print("| TRACK-CUSTOMER INFORMATION | ")
		print("-" * border, end = "\n\n")

		border = 140
		print("=" * border)
		print(f"{'Name':<30} {'Track':<30} {'Playlist':<30} {'Support Rep.':<30} {'Total':<30}")
		print("=" * border)

		for res in results:
			print(f"{res[0]:<30} {res[1]:<30} {res[2]:<30} {res[3]:<30} {res[4]:<30}")
		
		print("=" * border, end = "\n\n")

def main() -> None:
	clearSYS()
	searchTrackGenre()
	input("Press enter to continue...")

	clearSYS()
	printTrackBuyer()
	input("Press enter to continue...")

	clearSYS()
	printTrackPlaylist()
	input("Press enter to continue...")

	clearSYS()
	printTrackCustomer()
	input("Press enter to end...")

if __name__ == '__main__':
	main()
