from rest_framework import status
from rest_framework.response import Response


def actions(used_serializer, data, context, request, model):
    if request.method == 'GET':
        serializer = used_serializer(
            data=data,
            context=context,
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        querysetd = get_object_or_404(model,
                                      recipe=self.kwargs.get('pk'),
                                      fan=request.user)
        queryset.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
