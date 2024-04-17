package schema

import (
	"context"
	"fmt"
	"net/http"

	"github.com/vearch/vearch/sdk/go/v3/vearch/connection"
	"github.com/vearch/vearch/sdk/go/v3/vearch/except"
)

type SpaceDeleter struct {
	connection *connection.Connection
	dbName     string
	spaceName  string
}

func (dc *SpaceDeleter) WithDBName(dbName string) *SpaceDeleter {
	dc.dbName = dbName
	return dc
}

func (dc *SpaceDeleter) WithSpaceName(spaceName string) *SpaceDeleter {
	dc.spaceName = spaceName
	return dc
}

func (dc *SpaceDeleter) Do(ctx context.Context) error {
	responseData, err := dc.connection.RunREST(ctx, fmt.Sprintf("/dbs/%s/spaces/%s", dc.dbName, dc.spaceName), http.MethodDelete, nil)
	return except.CheckResponseDataErrorAndStatusCode(responseData, err, 200, 204)
}
